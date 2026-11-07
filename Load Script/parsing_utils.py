"""
Shared parsing helpers used by every source-specific loader.

Keeping these in one place means a fix to (say) the make-extraction regex
automatically improves all three sources at once, and the loaders themselves
stay short and readable.
"""
import re
import unicodedata
import pandas as pd
import numpy as np

from reference_data import (
    CANONICAL_MAKES, MAKE_ALIASES, MODEL_IMPLIES_MAKE,
    GOVERNORATE_ALIASES, CITY_TO_GOVERNORATE,
    FUEL_MAP, TRANSMISSION_MAP,
)

# Pre-sort alias keys longest-first so "land rover" matches before "land",
# and "mercedes-benz" before "mercedes".
_MAKE_ALIAS_KEYS_SORTED = sorted(MAKE_ALIASES.keys(), key=len, reverse=True)
_CITY_KEYS_SORTED = sorted(CITY_TO_GOVERNORATE.keys(), key=len, reverse=True)


def strip_accents(text: str) -> str:
    """'Citroën Médenine' -> 'citroen medenine' (lowercased, accent-free)."""
    if not isinstance(text, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    return no_accents.lower()


def extract_make_model(raw_title: str):
    """
    Best-effort extraction of (make, model) from a free-text listing title
    such as "Mercedes-Benz Classe C AMG" or "Hyandai Grand I 10 Première Main".

    Strategy (first match wins):
      1. normalize text (strip accents, lowercase, strip marketing fluff
         like "A Vendre", emojis, leading punctuation)
      2. try to match a known make alias at the START of the string
      3. fall back to searching for a known make ANYWHERE in the string
         (handles "Avendre Citroën C-Elysée Propre")
      4. fall back to MODEL_IMPLIES_MAKE for titles that only give the model
         (e.g. "Polo 4", "Golf 6 Gtd")
      5. give up -> ("Unknown", original cleaned title)

    Returns (make, model_text) where model_text is everything in the title
    that followed the matched make token (best-effort, can be empty).
    """
    if not isinstance(raw_title, str) or not raw_title.strip():
        return "Unknown", "Unknown"

    # strip emojis / decorative symbols and common "for sale" filler phrases
    cleaned = re.sub(r"[^\w\s\-éèêëàâôîïüûçÉÈÊËÀÂÔÎÏÜÛÇ./]", " ", raw_title)
    cleaned = re.sub(
        r"\b(a vendre|avendre|à vendre|vendre|urgent|occasion)\b",
        " ", cleaned, flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    norm = strip_accents(cleaned)

    # 2. prefix match
    for alias in _MAKE_ALIAS_KEYS_SORTED:
        if norm.startswith(alias):
            make = MAKE_ALIASES[alias]
            model = cleaned[len(alias):].strip(" -")
            return make, (model if model else "Unknown")

    # 3. anywhere-in-string match
    for alias in _MAKE_ALIAS_KEYS_SORTED:
        idx = norm.find(alias)
        if idx != -1:
            make = MAKE_ALIASES[alias]
            model = cleaned[idx + len(alias):].strip(" -")
            if not model:
                model = cleaned[:idx].strip(" -") or "Unknown"
            return make, model

    # 4. model-implies-make fallback (first word of the cleaned title)
    first_token = norm.split()[0] if norm.split() else ""
    first_token_alpha = re.sub(r"[^a-z]", "", first_token)
    if first_token_alpha in MODEL_IMPLIES_MAKE:
        return MODEL_IMPLIES_MAKE[first_token_alpha], cleaned

    # 5. give up
    return "Unknown", cleaned if cleaned else "Unknown"


def normalize_region(raw_region: str) -> str:
    """
    Map a free-text location string to one of Tunisia's 24 governorates,
    or 'Unknown' if nothing recognizable is found.
    Handles: exact governorate names, accented/cased variants, and
    city/suburb names embedded in longer address strings.
    """
    if not isinstance(raw_region, str) or not raw_region.strip():
        return "Unknown"

    norm = strip_accents(raw_region).strip()

    # direct governorate alias (most common case: source already gives the region)
    if norm in GOVERNORATE_ALIASES:
        result = GOVERNORATE_ALIASES[norm]
        return result

    # substring scan for a city/suburb keyword (handles full addresses)
    for city_key in _CITY_KEYS_SORTED:
        if city_key in norm:
            return CITY_TO_GOVERNORATE[city_key]

    # last resort: maybe a governorate name appears as a substring
    # (e.g. "Ariana - cité Riadh El Andalous", "Ben arous ville 24 631 900")
    for gov_key, gov_val in GOVERNORATE_ALIASES.items():
        if gov_key in norm and gov_val != "Unknown":
            return gov_val

    return "Unknown"


def parse_numeric(raw, strip_chars_pattern=r"[^0-9.]"):
    """Pull the numeric value out of strings like '220 000 km' or '75 000DT'."""
    if pd.isna(raw):
        return np.nan
    if isinstance(raw, (int, float)):
        return float(raw)
    s = re.sub(strip_chars_pattern, "", str(raw))
    if not s:
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def normalize_fuel(raw: str) -> str:
    if not isinstance(raw, str):
        return "Unknown"
    key = strip_accents(raw).strip()
    return FUEL_MAP.get(key, "Unknown")


def normalize_transmission(raw: str) -> str:
    if not isinstance(raw, str):
        return "Unknown"
    key = strip_accents(raw).strip()
    return TRANSMISSION_MAP.get(key, "Unknown")


def flag_mileage_outlier(km: float) -> bool:
    """
    Heuristic sanity check: a used car's odometer in Tunisia realistically
    falls under ~600,000 km. Scraped placeholder/garbage values we actually
    observed: 999999, 17000000, 11111111 — these are obvious sentinel/typo
    values, not real readings.
    """
    if pd.isna(km):
        return False
    return km <= 0 or km > 600_000


def flag_price_outlier(price: float) -> bool:
    """
    Heuristic bounds for the Tunisian used-car market (in TND). Anything
    below ~1,000 TND is almost certainly a parts/wreck listing or scrape
    error; above ~600,000 TND is a luxury exotic, rare but real, so we flag
    rather than drop it.
    """
    if pd.isna(price):
        return False
    return price < 1_000 or price > 600_000
