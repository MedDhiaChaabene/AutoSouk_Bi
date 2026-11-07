"""
Loader for automobile_all_pages.csv (source: automobile.tn)

Source-specific quirks handled here:
  - 'thumb-caption' holds the full title ("Mercedes-Benz Classe C AMG") ->
    split into make/model via parsing_utils.extract_make_model.
  - 'road' is mileage as "220 000 km" -> parsed to a float.
  - 'price' is "75 000DT" (sometimes with a prefix like "Sous leasing" or
    "Non dédouané" glued on) -> numeric extraction strips all non-digits
    so this still works.
  - 'fw-medium' is actually the region/governorate (oddly named column from
    the scrape tool, kept as the raw header), already fairly clean.
  - 'cote-appreciation' is the site's own deal-quality verdict -> kept as
    source_deal_label (a feature/baseline, NOT our target).
  - 'occasion-link-overlay href' points to the DEALER'S storefront for ~988
    rows (when a 'seller href' is present) rather than a true per-listing
    permalink. This is a scraper limitation on dealer pages, not duplicate
    listings - each such row is still a distinct car. We build a synthetic
    listing_id from the row's position to keep every row addressable, since
    no other column is unique either.
  - 'seller href' non-null => dealer/pro listing; null => private seller.
  - 'thumb-caption (2)' is 100% null - dropped, not used.
"""
import pandas as pd

from parsing_utils import (
    extract_make_model, parse_numeric, normalize_region,
    normalize_fuel, normalize_transmission,
    flag_price_outlier, flag_mileage_outlier,
)
from schema import UNIFIED_COLUMNS


def load_automobile_tn(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)

    out = pd.DataFrame(index=raw.index)
    out["listing_id"] = "automobile_tn_" + raw.index.astype(str)
    out["source"] = "automobile_tn"
    out["title_raw"] = raw["thumb-caption"]

    make_model = raw["thumb-caption"].apply(extract_make_model)
    out["make"] = make_model.apply(lambda x: x[0])
    out["model"] = make_model.apply(lambda x: x[1])

    out["year"] = raw["year"].astype(float)
    out["price_tnd"] = raw["price"].apply(parse_numeric)
    out["mileage_km"] = raw["road"].apply(parse_numeric)
    out["fuel_type"] = raw["fuel"].apply(normalize_fuel)
    # 'boite' (Automatique/Manuelle) is the real transmission-type column here;
    # 'transmission' in this source actually means drivetrain (Traction/
    # Propulsion/Intégrale) which is a different concept - not mapped.
    out["transmission"] = raw["boite"].apply(normalize_transmission)
    out["body_type"] = "Unknown"  # not provided by this source
    out["region"] = raw["fw-medium"].apply(normalize_region)
    out["seller_type"] = raw["seller href"].notna().map({True: "Pro", False: "Private"})
    out["listing_date"] = raw["listing_date"]
    out["source_deal_label"] = raw["cote-appreciation"]
    out["listing_url"] = raw["occasion-link-overlay href"]

    out["is_price_outlier"] = out["price_tnd"].apply(flag_price_outlier)
    out["is_mileage_outlier"] = out["mileage_km"].apply(flag_mileage_outlier)

    return out[UNIFIED_COLUMNS]


if __name__ == "__main__":
    df = load_automobile_tn("/mnt/user-data/uploads/automobile_all_pages.csv")
    print(df.shape)
    print(df.head(10).to_string())
    print()
    print("make Unknown rate:", (df["make"] == "Unknown").mean())
    print("region Unknown rate:", (df["region"] == "Unknown").mean())
    print("price outliers:", df["is_price_outlier"].sum())
    print("mileage outliers:", df["is_mileage_outlier"].sum())
