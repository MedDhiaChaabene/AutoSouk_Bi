"""
Main entry point: loads all three sources, unifies them into one table,
runs cross-source sanity checks, and writes the final CSV.

Usage:
    python main.py
"""
import pandas as pd

from load_automobile_tn import load_automobile_tn
from load_baniola_tn import load_baniola_tn
from load_scoutcar_tn import load_scoutcar_tn
from schema import UNIFIED_COLUMNS

AUTOMOBILE_PATH = "/mnt/user-data/uploads/automobile_all_pages.csv"
BANIOLA_PATH = "/mnt/user-data/uploads/baniola_cars_full.csv"
SCOUTCAR_PATH = "/mnt/user-data/uploads/scoutcar_all_listings.csv"

# Baniola's 'posted' field is relative ("Il y a 1 semaine") with no absolute
# timestamp in the source data. We anchor it to the latest listing_date seen
# across the other two (clean, absolute-dated) sources, which is a
# reasonable proxy for "when this combined scrape was actually run".
def _infer_as_of_date(*absolute_date_series) -> str:
    all_dates = pd.concat([pd.to_datetime(s, errors="coerce") for s in absolute_date_series])
    return all_dates.max().strftime("%Y-%m-%d")


def build_unified_table() -> pd.DataFrame:
    auto_df = load_automobile_tn(AUTOMOBILE_PATH)
    scout_df = load_scoutcar_tn(SCOUTCAR_PATH)

    as_of_date = _infer_as_of_date(auto_df["listing_date"], scout_df["listing_date"])
    print(f"[info] inferred as-of date for baniola relative dates: {as_of_date}")

    baniola_df = load_baniola_tn(BANIOLA_PATH, as_of_date=as_of_date)

    unified = pd.concat([auto_df, baniola_df, scout_df], ignore_index=True)
    unified = unified[UNIFIED_COLUMNS]
    return unified


def run_sanity_checks(df: pd.DataFrame) -> None:
    print("\n=== UNIFIED TABLE SANITY REPORT ===")
    print(f"Total rows: {len(df)}")
    print("\nRows per source:")
    print(df["source"].value_counts())

    print("\nNull / 'Unknown' rates per key column:")
    for col in ["make", "region", "fuel_type", "transmission", "body_type", "seller_type"]:
        unknown_rate = (df[col] == "Unknown").mean()
        print(f"  {col:15s}: {unknown_rate:6.1%} Unknown")

    print(f"\nMissing price_tnd (e.g. 'Prix sur demande'): {df['price_tnd'].isna().mean():.1%}")
    print(f"Missing mileage_km:                          {df['mileage_km'].isna().mean():.1%}")
    print(f"Missing year:                                {df['year'].isna().mean():.1%}")

    print(f"\nFlagged price outliers:   {df['is_price_outlier'].sum()} rows")
    print(f"Flagged mileage outliers: {df['is_mileage_outlier'].sum()} rows")

    print("\nYear range:", df["year"].min(), "-", df["year"].max())
    print("Price range (TND), excluding outliers:")
    clean_price = df.loc[~df["is_price_outlier"], "price_tnd"]
    print(clean_price.describe())

    dup_url_count = df["listing_url"].duplicated().sum()
    print(f"\nDuplicate listing_url across the unified table: {dup_url_count}")
    print("(expected: >0, since automobile.tn's dealer rows share a storefront URL")
    print(" instead of a per-listing permalink - these are still distinct cars, not")
    print(" true duplicates; see load_automobile_tn.py docstring)")

    print("\nTop 10 makes overall:")
    print(df["make"].value_counts().head(10))

    print("\nRows per region:")
    print(df["region"].value_counts())


if __name__ == "__main__":
    unified = build_unified_table()
    run_sanity_checks(unified)

    out_path = "/mnt/user-data/outputs/unified_car_listings.csv"
    unified.to_csv(out_path, index=False)
    print(f"\n[done] wrote {len(unified)} rows to {out_path}")
