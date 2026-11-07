"""
The canonical unified schema every source gets mapped into.

This is intentionally a flat, denormalized "fact table" rather than a
multi-table star schema: for a project that feeds straight into
pandas/scikit-learn, one clean CSV is far more useful than a normalized
relational layout. (If you DO want dim tables for a reporting/BI angle,
dim_make, dim_region and dim_source can be trivially derived by taking
.unique() on the relevant columns of this table — see step 4 in main.py.)

Column reference
-----------------
listing_id        str   : unique ID within source, prefixed by source name
                          (so it stays globally unique after concatenation)
source            str   : 'automobile_tn' | 'baniola_tn' | 'scoutcar_tn'
title_raw         str   : original scraped title/caption, kept for audit/debug
make              str   : canonical make, e.g. 'Volkswagen' (or 'Unknown')
model             str   : best-effort model text (free text, not canonicalized
                          further - model normalization is a good v2 task)
year              float : manufacturing year
price_tnd         float : listing price in Tunisian Dinar
mileage_km        float : odometer reading in km
fuel_type         str   : 'Petrol' | 'Diesel' | 'Hybrid' | 'Electric' | 'LPG' | 'Unknown'
transmission      str   : 'Automatic' | 'Manual' | 'CVT' | 'Unknown'
body_type         str   : free text body/category, only populated by ScoutCar
                          today (others -> 'Unknown')
region             str  : one of the 24 Tunisian governorates, or 'Unknown'
seller_type       str   : 'Pro' | 'Private' | 'Unknown'
listing_date      str   : ISO date (YYYY-MM-DD) the ad was posted/scraped, if known
source_deal_label str   : the SOURCE SITE's own "is this a good price" verdict,
                          where available (automobile.tn's cote-appreciation,
                          baniola's estimation). NOT our target label - kept
                          as a feature / sanity-check baseline only.
listing_url       str   : link back to the original ad
is_price_outlier  bool  : True if price_tnd looks like a data-quality problem
is_mileage_outlier bool : True if mileage_km looks like a data-quality problem
"""

UNIFIED_COLUMNS = [
    "listing_id", "source", "title_raw", "make", "model", "year",
    "price_tnd", "mileage_km", "fuel_type", "transmission", "body_type",
    "region", "seller_type", "listing_date", "source_deal_label",
    "listing_url", "is_price_outlier", "is_mileage_outlier",
]
