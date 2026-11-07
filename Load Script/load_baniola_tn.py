"""
Loader for baniola_cars_full.csv (source: baniola.tn)

Source-specific quirks handled here:
  - 'title' is the free-text listing title, much noisier than automobile.tn's
    (emojis, typos, missing make, Arabic script in a few rows) -> split via
    the same extract_make_model helper; lower match rate expected (~98%).
  - 'price_raw' / 'price_dt': price_dt is already a parsed float, EXCEPT for
    342 rows where the seller chose "Prix sur demande" (price on request) ->
    these become NaN, which is correct (we genuinely don't know the price).
    Rows with missing price are dropped further downstream for the
    regression targets, but kept here with NaN since they may still carry
    useful info for other purposes (e.g. depreciation feature engineering
    on non-price fields). Decide at modeling time whether to drop them.
  - 'gearbox', 'negotiable', 'exchange' are 100% null in this scrape (dead
    columns / broken selectors) - not mapped.
  - 'posted' is a RELATIVE date string ("Il y a 1 semaine") rather than an
    absolute date. We convert it to an absolute date using `as_of_date`,
    the date the scrape is assumed to have run. Since this source has no
    embedded absolute timestamp, this conversion is necessarily approximate
    (e.g. "Il y a 1 semaine" could mean anywhere from 7-13 days, as the site
    only buckets into "1 semaine" up to "2 semaines" etc.) - treat
    listing_date for this source as lower-precision than the other two.
  - 'estimation' is this site's own deal-quality verdict (Bonne affaire /
    Très cher / etc., 53% null) -> kept as source_deal_label.
  - 'region' is already fairly clean Tunisian governorate names with minor
    casing/accent differences -> normalize_region handles it.
  - No seller_type / pro-vs-private signal exists in this source -> 'Unknown'.
  - No body_type signal -> 'Unknown'.
  - 102 exact full-row duplicates exist (likely re-scraped on consecutive
    runs) -> dropped here before returning.
"""
import re
import pandas as pd

from parsing_utils import (
    extract_make_model, parse_numeric, normalize_region,
    normalize_fuel, flag_price_outlier, flag_mileage_outlier,
)
from schema import UNIFIED_COLUMNS

_RELATIVE_DATE_RE = re.compile(
    r"il y a (\d+) (minute|minutes|heure|heures|jour|jours|semaine|semaines)",
    re.IGNORECASE,
)
_UNIT_TO_DAYS = {
    "minute": 0, "minutes": 0,        # same day
    "heure": 0, "heures": 0,          # same day
    "jour": 1, "jours": 1,
    "semaine": 7, "semaines": 7,
}


def _relative_to_absolute_date(posted: str, as_of_date: pd.Timestamp):
    if not isinstance(posted, str):
        return pd.NaT
    m = _RELATIVE_DATE_RE.search(posted.lower())
    if not m:
        return pd.NaT
    qty, unit = int(m.group(1)), m.group(2)
    days_back = qty * _UNIT_TO_DAYS.get(unit, 0)
    return as_of_date - pd.Timedelta(days=days_back)


def load_baniola_tn(path: str, as_of_date: str = None) -> pd.DataFrame:
    raw = pd.read_csv(path)
    raw = raw.drop_duplicates()  # 102 exact dupes, likely re-scrape artifacts

    if as_of_date is None:
        # No absolute date in this source; default to "today" at pipeline
        # run time. Pass an explicit as_of_date for reproducible runs.
        as_of_date = pd.Timestamp.today().normalize()
    else:
        as_of_date = pd.Timestamp(as_of_date)

    out = pd.DataFrame(index=raw.index)
    out["listing_id"] = "baniola_tn_" + raw.index.astype(str)
    out["source"] = "baniola_tn"
    out["title_raw"] = raw["title"]

    make_model = raw["title"].apply(extract_make_model)
    out["make"] = make_model.apply(lambda x: x[0])
    out["model"] = make_model.apply(lambda x: x[1])

    out["year"] = raw["year"].astype(float)
    out["price_tnd"] = raw["price_dt"]  # already numeric; NaN = "Prix sur demande"
    out["mileage_km"] = raw["km_num"]
    out["fuel_type"] = raw["fuel"].apply(normalize_fuel)
    out["transmission"] = "Unknown"  # 'gearbox' column is 100% null in this scrape
    out["body_type"] = "Unknown"
    out["region"] = raw["region"].apply(normalize_region)
    out["seller_type"] = "Unknown"  # no pro/private signal in this source
    out["listing_date"] = raw["posted"].apply(
        lambda p: _relative_to_absolute_date(p, as_of_date)
    ).dt.strftime("%Y-%m-%d")
    out["source_deal_label"] = raw["estimation"]
    out["listing_url"] = raw["url"]

    out["is_price_outlier"] = out["price_tnd"].apply(flag_price_outlier)
    out["is_mileage_outlier"] = out["mileage_km"].apply(flag_mileage_outlier)

    return out[UNIFIED_COLUMNS]


if __name__ == "__main__":
    df = load_baniola_tn(
        "/mnt/user-data/uploads/baniola_cars_full.csv", as_of_date="2026-06-27"
    )
    print(df.shape)
    print(df.head(10).to_string())
    print()
    print("make Unknown rate:", (df["make"] == "Unknown").mean())
    print("region Unknown rate:", (df["region"] == "Unknown").mean())
    print("price_tnd null rate (Prix sur demande):", df["price_tnd"].isna().mean())
    print("price outliers:", df["is_price_outlier"].sum())
    print("mileage outliers:", df["is_mileage_outlier"].sum())
