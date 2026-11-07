"""
Loader for scoutcar_all_listings.csv (source: scoutcar.tn)

Source-specific quirks handled here:
  - This is the only source with pre-split 'make' / 'model' columns already
    -> we still run make through the alias table (normalize_make) to align
    spelling/casing with the other two sources (e.g. so 'Citroen' from here
    matches 'Citroën'-derived 'Citroen' from automobile.tn/baniola).
  - 'localisation' is messy free text (mixed case, typos, embedded street
    addresses, "city, Tunisie"/"city, Tunisia"/"city" inconsistently) ->
    normalize_region's substring/city-keyword matching handles most of it
    (~97% match rate); the rest fall to 'Unknown'.
  - 'transmission' mixes French/English labels ('Manuelle', 'Automatic',
    'Manual', 'CVT') plus one literal "0" (scrape glitch) -> normalized.
  - 'carrosserie' (body type) is a clean, pre-existing taxonomy (Compacte,
    SUV, Sedan, Pickup, ...) -> kept almost as-is, just null-filled.
  - 'condition' and 'category' are 100% null - dropped, not used.
  - 'is_pro' is 100% False for every row (broken scrape selector, not a
    real signal) -> NOT used for seller_type. We fall back to
    'author_name' presence as a weak proxy (every row has either a personal
    name or a dealer-style name in this field, so this alone can't really
    distinguish pro/private) -> seller_type left as 'Unknown' here too,
    matching baniola. (vendor_url existing for ~all rows doesn't help
    either, since both private sellers and dealers get a vendor page.)
  - 'status': 'publish' (active) vs 'vendu' (sold) -> sold listings carry
    a REALIZED price, not just an asking price, which can be a valuable
    signal for the fair-price model. Exposed via source_deal_label since
    there's no native "good deal" verdict here, so we repurpose that column
    to carry "Vendu"/"En vente" rather than leaving it NaN. Flag this if
    you want to keep the deal-label column source-comparable instead - see
    note in main.py.
  - 'post_date' is already a clean absolute timestamp -> just reformatted.
"""
import pandas as pd

from parsing_utils import (
    strip_accents, normalize_region, flag_price_outlier, flag_mileage_outlier,
)
from reference_data import MAKE_ALIASES
from schema import UNIFIED_COLUMNS

_TRANSMISSION_MAP = {
    "automatic": "Automatic", "manuelle": "Manual", "manual": "Manual", "cvt": "CVT",
}


def _normalize_make(raw_make: str) -> str:
    if not isinstance(raw_make, str) or not raw_make.strip():
        return "Unknown"
    key = strip_accents(raw_make).strip()
    return MAKE_ALIASES.get(key, raw_make.strip())  # keep original if not in alias table


def _normalize_transmission(raw: str) -> str:
    if not isinstance(raw, str):
        return "Unknown"
    return _TRANSMISSION_MAP.get(strip_accents(raw).strip(), "Unknown")


def load_scoutcar_tn(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)

    out = pd.DataFrame(index=raw.index)
    out["listing_id"] = "scoutcar_tn_" + raw["id"].astype(str)
    out["source"] = "scoutcar_tn"
    out["title_raw"] = raw["title"]

    out["make"] = raw["make"].apply(_normalize_make)
    out["model"] = raw["model"]

    out["year"] = raw["annee"].astype(float)
    out["price_tnd"] = raw["prix"].astype(float)
    out["mileage_km"] = raw["kilometrage"].astype(float)
    out["fuel_type"] = raw["carburant"].apply(
        lambda x: {"essence": "Petrol", "diesel": "Diesel", "hybrid": "Hybrid",
                   "electrique": "Electric", "gpl": "LPG",
                   "essence/gpl": "LPG"}.get(strip_accents(x).strip() if isinstance(x, str) else "", "Unknown")
    )
    out["transmission"] = raw["transmission"].apply(_normalize_transmission)
    out["body_type"] = raw["carrosserie"].fillna("Unknown")
    out["region"] = raw["localisation"].apply(normalize_region)
    out["seller_type"] = "Unknown"  # 'is_pro' is a broken/always-False column in this scrape
    out["listing_date"] = pd.to_datetime(raw["post_date"]).dt.strftime("%Y-%m-%d")
    # No native deal-quality verdict on this source; repurpose this column to
    # carry sold-vs-active status instead (still useful context, just not
    # directly comparable to the other two sources' price-quality labels).
    out["source_deal_label"] = raw["status"].map({"publish": "En vente", "vendu": "Vendu"})
    out["listing_url"] = raw["permalink"]

    out["is_price_outlier"] = out["price_tnd"].apply(flag_price_outlier)
    out["is_mileage_outlier"] = out["mileage_km"].apply(flag_mileage_outlier)

    return out[UNIFIED_COLUMNS]


if __name__ == "__main__":
    df = load_scoutcar_tn("/mnt/user-data/uploads/scoutcar_all_listings.csv")
    print(df.shape)
    print(df.head(10).to_string())
    print()
    print("make Unknown rate:", (df["make"] == "Unknown").mean())
    print("region Unknown rate:", (df["region"] == "Unknown").mean())
    print("price outliers:", df["is_price_outlier"].sum())
    print("mileage outliers:", df["is_mileage_outlier"].sum())
    print(df["source_deal_label"].value_counts())
