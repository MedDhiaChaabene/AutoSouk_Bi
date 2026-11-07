"""
Reference data shared across all three source loaders:
  - canonical list of car makes (+ aliases / common misspellings -> canonical form)
  - canonical list of Tunisian governorates (+ city/suburb -> governorate mapping)
  - canonical fuel / transmission / body-type vocabularies

This file is the single place to extend coverage when you see a new
"Unknown" show up after running the pipeline on a fresh scrape.
"""

# ---------------------------------------------------------------------------
# 1. MAKES
# ---------------------------------------------------------------------------
# Canonical taxonomy borrowed from ScoutCar (it had clean, pre-split make/model
# columns), extended with a few makes seen only in the other two sources.
CANONICAL_MAKES = sorted(set([
    "Alfa Romeo", "Audi", "BMW", "BYD", "Baic", "Chery", "Chevrolet", "Citroen",
    "Cupra", "DS", "Dacia", "DongFeng", "FAW", "Fiat", "Ford", "Foton", "GMC",
    "Geely", "Great Wall", "Haval", "Honda", "Hummer", "Hyundai", "Infiniti",
    "Isuzu", "Jaguar", "Jeep", "Kia", "Lancia", "Land Rover", "Lynk & Co", "MG",
    "Mahindra", "Mazda", "Mercedes-Benz", "Mini", "Mitsubishi", "Nissan", "Opel",
    "Peugeot", "Porsche", "Renault", "SEAT", "Skoda", "Smart", "SsangYong",
    "Suzuki", "Tata", "Tesla", "Toyota", "Volkswagen", "Volvo",
    # additions seen in automobile.tn / baniola but absent from ScoutCar's list
    "GWM", "DFSK", "GAC", "Wallyscar", "Subaru", "Lexus", "Chrysler", "Daewoo",
    "Daihatsu", "Rolls-Royce", "Bentley", "Maserati", "Abarth",
    "Lada", "Changan", "Cadillac", "JAC", "Omoda", "Jaecoo", "Iveco",
]))

# alias / common-spelling-variant -> canonical make.
# Keys are matched on a lowercased, accent-stripped string.
MAKE_ALIASES = {
    "citroen": "Citroen", "citroën": "Citroen",
    "mercedes": "Mercedes-Benz", "mercedes-benz": "Mercedes-Benz", "mercedez": "Mercedes-Benz",
    "vw": "Volkswagen", "volkswagen": "Volkswagen", "volkswagon": "Volkswagen",
    "skoda": "Skoda", "škoda": "Skoda",
    "hyundai": "Hyundai", "hyandai": "Hyundai", "hyndai": "Hyundai",
    "peugeot": "Peugeot", "peugot": "Peugeot", "peugote": "Peugeot",
    "gwm": "GWM", "great wall": "GWM", "haval": "Haval",  # Haval kept separate: it's GWM's sub-brand but ads use it as the "make"
    "kia": "Kia",
    "renault": "Renault",
    "landrover": "Land Rover", "land rover": "Land Rover", "land-rover": "Land Rover",
    "ssangyong": "SsangYong", "ssang yong": "SsangYong",
    "seat": "SEAT",
    "bmw": "BMW",
    "mg": "MG",
    "byd": "BYD",
    "mahindra": "Mahindra", "mahdra": "Mahindra",
    "chery": "Chery",
    "dacia": "Dacia",
    "fiat": "Fiat",
    "ford": "Ford",
    "opel": "Opel",
    "nissan": "Nissan",
    "toyota": "Toyota",
    "mazda": "Mazda",
    "audi": "Audi",
    "jeep": "Jeep",
    "isuzu": "Isuzu",
    "suzuki": "Suzuki",
    "porsche": "Porsche",
    "jaguar": "Jaguar",
    "mitsubishi": "Mitsubishi",
    "chevrolet": "Chevrolet", "chevy": "Chevrolet",
    "infiniti": "Infiniti",
    "honda": "Honda",
    "tesla": "Tesla",
    "volvo": "Volvo",
    "mini": "Mini",
    "smart": "Smart",
    "hummer": "Hummer",
    "gmc": "GMC",
    "geely": "Geely",
    "dfsk": "DFSK",
    "gac": "GAC",
    "wallyscar": "Wallyscar",
    "lynk & co": "Lynk & Co", "lynk and co": "Lynk & Co", "lynkco": "Lynk & Co",
    "cupra": "Cupra",
    "ds": "DS",
    "tata": "Tata",
    "lancia": "Lancia",
    "alfa romeo": "Alfa Romeo", "alfaromeo": "Alfa Romeo",
    "subaru": "Subaru",
    "lexus": "Lexus",
    "chrysler": "Chrysler",
    "daewoo": "Daewoo",
    "daihatsu": "Daihatsu",
    "rolls-royce": "Rolls-Royce", "rolls royce": "Rolls-Royce",
    "bentley": "Bentley",
    "maserati": "Maserati",
    "abarth": "Abarth",
    "dongfeng": "DongFeng",
    "faw": "FAW",
    "foton": "Foton",
    # extra makes / common typos observed in automobile.tn & baniola titles
    "lada": "Lada", "changan": "Changan", "cadillac": "Cadillac", "jac": "JAC",
    "omoda": "Omoda", "omoda & jaecoo": "Omoda", "jaecoo": "Jaecoo",
    "iveco": "Iveco",
    "oppel": "Opel",  # typo
    "reneaut": "Renault", "renaut": "Renault",  # typos
    "pssat": "Volkswagen",  # "Pssat" = typo'd model "Passat", make implied
    "tayota": "Toyota",  # typo
    "bmm": "BMW",  # typo
    "ssangyan": "SsangYong", "sang yong": "SsangYong", "tivoli sang yong": "SsangYong",  # typo/variant
}

# Some listings use a MODEL name as if it were the title's first word, with no
# make mentioned at all (e.g. "Polo 4", "Golf 6 Gtd", "Symbole1"). For these,
# the model itself implies the make. Used only as a last-resort fallback.
MODEL_IMPLIES_MAKE = {
    "polo": "Volkswagen", "golf": "Volkswagen", "passat": "Volkswagen",
    "jetta": "Volkswagen", "tiguan": "Volkswagen", "vento": "Volkswagen",
    "clio": "Renault", "megane": "Renault", "symbol": "Renault", "symbole": "Renault",
    "kangoo": "Renault", "laguna": "Renault", "koleos": "Renault",
    "208": "Peugeot", "207": "Peugeot", "206": "Peugeot", "2008": "Peugeot",
    "308": "Peugeot", "3008": "Peugeot", "partner": "Peugeot", "407": "Peugeot",
    "i10": "Hyundai", "i20": "Hyundai", "i30": "Hyundai", "tucson": "Hyundai",
    "octavia": "Skoda", "fabia": "Skoda", "superb": "Skoda", "kamiq": "Skoda",
    "corolla": "Toyota", "yaris": "Toyota", "rav4": "Toyota", "hilux": "Toyota",
    "sportage": "Kia", "picanto": "Kia", "rio": "Kia", "ceed": "Kia",
    "tiggo": "Chery",
    "duster": "Dacia", "sandero": "Dacia", "logan": "Dacia",
    "swift": "Suzuki", "jimny": "Suzuki",
    "qashqai": "Nissan", "micra": "Nissan", "juke": "Nissan",
    "ibiza": "SEAT", "leon": "SEAT",
    "207": "Peugeot", "206": "Peugeot",
    "c3": "Citroen", "c4": "Citroen", "c5": "Citroen", "berlingo": "Citroen",
    "caddy": "Volkswagen", "punto": "Fiat", "500": "Fiat", "panda": "Fiat",
}

# ---------------------------------------------------------------------------
# 2. GOVERNORATES (Tunisia's 24 administrative regions)
# ---------------------------------------------------------------------------
CANONICAL_GOVERNORATES = [
    "Tunis", "Ariana", "Ben Arous", "Manouba", "Nabeul", "Zaghouan", "Bizerte",
    "Béja", "Jendouba", "Le Kef", "Siliana", "Sousse", "Monastir", "Mahdia",
    "Sfax", "Kairouan", "Kasserine", "Sidi Bouzid", "Gabès", "Médenine",
    "Tataouine", "Gafsa", "Tozeur", "Kébili",
]

# Direct governorate-name variants (accents / casing / spelling) -> canonical.
GOVERNORATE_ALIASES = {
    "tunis": "Tunis", "tunisia": "Unknown", "tunisie": "Unknown",  # "Tunisie" alone = country, not a region
    "ariana": "Ariana", "arianna": "Ariana", "ariane": "Ariana",
    "ben arous": "Ben Arous", "benarous": "Ben Arous",
    "manouba": "Manouba", "la manouba": "Manouba",
    "nabeul": "Nabeul",
    "zaghouan": "Zaghouan",
    "bizerte": "Bizerte",
    "beja": "Béja", "béja": "Béja",
    "jendouba": "Jendouba",
    "kef": "Le Kef", "le kef": "Le Kef",
    "siliana": "Siliana",
    "sousse": "Sousse",
    "monastir": "Monastir",
    "mahdia": "Mahdia",
    "sfax": "Sfax",
    "kairouan": "Kairouan",
    "kasserine": "Kasserine",
    "sidi bouzid": "Sidi Bouzid", "sidi-bouzid": "Sidi Bouzid",
    "gabes": "Gabès", "gabès": "Gabès",
    "medenine": "Médenine", "médenine": "Médenine",
    "tataouine": "Tataouine",
    "gafsa": "Gafsa",
    "tozeur": "Tozeur",
    "kebili": "Kébili", "kébili": "Kébili",
}

# City / suburb / neighborhood keywords -> governorate. Checked via substring
# containment, longest keyword first, against a lowercased & accent-stripped
# address string (handles ScoutCar's free-text "localisation" column, e.g.
# "11 rue el kods menzah 8 Ariana" or "Ben arous mourouj 4").
CITY_TO_GOVERNORATE = {
    # Tunis governorate
    "la marsa": "Tunis", "marsa": "Tunis", "carthage": "Tunis", "bardo": "Tunis",
    "le bardo": "Tunis", "el menzah": "Tunis", "menzah": "Tunis", "ennasr": "Tunis",
    "el manar": "Tunis", "cite jardins": "Tunis", "bab bhar": "Tunis",
    "mutuelle ville": "Tunis", "lac 1": "Tunis", "lac 2": "Tunis", "les berges du lac": "Tunis",
    "el omrane": "Tunis", "el kabaria": "Tunis", "bab souika": "Tunis",
    "sidi bechir": "Tunis", "khaznadar": "Tunis", "el ouardia": "Tunis",
    # Ariana governorate
    "ariana": "Ariana", "soukra": "Ariana", "la soukra": "Ariana",
    "raoued": "Ariana", "ettadhamen": "Ariana", "mnihla": "Ariana",
    "andalous": "Ariana", "riadh el andalous": "Ariana", "ghazela": "Ariana",
    "borj louzir": "Ariana",
    # Ben Arous governorate
    "ben arous": "Ben Arous", "rades": "Ben Arous", "rad\u00e8s": "Ben Arous",
    "ezzahra": "Ben Arous", "hammam lif": "Ben Arous", "hammam chott": "Ben Arous",
    "mourouj": "Ben Arous", "el mourouj": "Ben Arous", "mohamedia": "Ben Arous",
    "borj cedria": "Ben Arous", "fouchana": "Ben Arous", "megrine": "Ben Arous",
    "boumhel": "Ben Arous", "mhamdia": "Ben Arous",
    # Manouba governorate
    "manouba": "Manouba", "denden": "Manouba", "oued ellil": "Manouba",
    "douar hicher": "Manouba", "tebourba": "Manouba",
    # Nabeul governorate
    "nabeul": "Nabeul", "hammamet": "Nabeul", "grombalia": "Nabeul",
    "kelibia": "Nabeul", "menzel temime": "Nabeul", "korba": "Nabeul",
    "dar chaabane": "Nabeul", "beni khalled": "Nabeul",
    # Zaghouan
    "zaghouan": "Zaghouan", "el fahs": "Zaghouan",
    # Bizerte
    "bizerte": "Bizerte", "menzel bourguiba": "Bizerte", "menzel jemil": "Bizerte",
    "mateur": "Bizerte", "ras jebel": "Bizerte", "ghar el melh": "Bizerte",
    # Beja
    "beja": "Béja", "medjez el bab": "Béja", "testour": "Béja",
    # Jendouba
    "jendouba": "Jendouba", "tabarka": "Jendouba", "ain draham": "Jendouba",
    # Le Kef
    "kef": "Le Kef", "le kef": "Le Kef",
    # Siliana
    "siliana": "Siliana",
    # Sousse
    "sousse": "Sousse", "akouda": "Sousse", "hammam sousse": "Sousse",
    "kalaa kebira": "Sousse", "msaken": "Sousse", "kantaoui": "Sousse",
    "port el kantaoui": "Sousse",
    # Monastir
    "monastir": "Monastir", "skanes": "Monastir", "ksar hellal": "Monastir",
    "jemmal": "Monastir", "ksibet": "Monastir", "moknine": "Monastir",
    # Mahdia
    "mahdia": "Mahdia", "el jem": "Mahdia",
    # Sfax
    "sfax": "Sfax", "sakiet": "Sfax", "thyna": "Sfax",
    # Kairouan
    "kairouan": "Kairouan",
    # Kasserine
    "kasserine": "Kasserine",
    # Sidi Bouzid
    "sidi bouzid": "Sidi Bouzid",
    # Gabes
    "gabes": "Gabès", "gabès": "Gabès",
    # Medenine
    "medenine": "Médenine", "médenine": "Médenine", "djerba": "Médenine",
    "jerba": "Médenine", "houmt souk": "Médenine", "zarzis": "Médenine",
    "ben gardane": "Médenine", "ben guerdane": "Médenine", "benguerdane": "Médenine",
    # Tataouine
    "tataouine": "Tataouine",
    # Gafsa
    "gafsa": "Gafsa",
    # Tozeur
    "tozeur": "Tozeur",
    # Kebili
    "kebili": "Kébili", "douz": "Kébili",
    # additional cities / common typos observed in ScoutCar's free-text localisation field
    "mannouba": "Manouba", "kram": "Tunis", "le kram": "Tunis",
    "eljem": "Mahdia", "el jem": "Mahdia",
    "teboulba": "Monastir", "ksour essef": "Mahdia",
    "boumhal": "Ben Arous", "morneg": "Ben Arous", "mornag": "Ben Arous",
    "jandouba": "Jendouba", "ariena": "Ariana", "bizert": "Bizerte",
    "feriana": "Kasserine", "gremda": "Sfax", "grombelia": "Nabeul",
    "hammem lif": "Ben Arous", "borj el amri": "Manouba", "makther": "Siliana",
    "menzeh": "Tunis",
}

# ---------------------------------------------------------------------------
# 3. FUEL / TRANSMISSION / BODY TYPE vocab
# ---------------------------------------------------------------------------
FUEL_MAP = {
    "essence": "Petrol", "diesel": "Diesel", "hybride": "Hybrid", "hybrid": "Hybrid",
    "electrique": "Electric", "électrique": "Electric", "gpl": "LPG",
    "essence/gpl": "LPG",
}

TRANSMISSION_MAP = {
    "automatique": "Automatic", "automatic": "Automatic", "auto": "Automatic",
    "manuelle": "Manual", "manual": "Manual", "manuel": "Manual",
    "cvt": "CVT",
}
