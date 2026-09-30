"""
Sample "Krishi Seva Kendra" (agri-input shop) directory, keyed by district.

This is a curated SAMPLE directory for demo/pilot purposes -- not a live
listings feed. For production, replace `get_shops_for_district()` with a
call to a real local-business API (e.g. Google Places API with a district
bounding box) or let admins manage entries via the Admin Panel using the
`agri_shops` DB table pattern (add a model similar to Disease if desired).
"""

# A few illustrative sample entries. Extend this dict with more
# districts/shops, or swap the whole function for a real API/DB lookup.
SAMPLE_AGRI_SHOPS = {
    "Nanded": [
        {"name": "Shivshakti Krishi Seva Kendra", "address": "Vazirabad Road, Nanded", "phone": "+919421012345"},
        {"name": "Nanded Agro Center", "address": "Shivaji Nagar, Nanded", "phone": "+919876512340"},
        {"name": "Krishi Sampada Agencies", "address": "Degloor Naka, Nanded", "phone": "+919922334455"},
    ],
    "Pune": [
        {"name": "Pune Krishi Kendra", "address": "Shivaji Nagar, Pune", "phone": "+919812345670"},
        {"name": "Green Field Agro Supplies", "address": "Hadapsar, Pune", "phone": "+919823456781"},
    ],
    "Nashik": [
        {"name": "Nashik Krishi Seva Kendra", "address": "College Road, Nashik", "phone": "+919834567892"},
    ],
}

DEFAULT_SHOPS = [
    {"name": "Local Krishi Seva Kendra", "address": "Visit your nearest APMC market for agri-input shops", "phone": None},
]


def get_shops_for_district(district: str):
    if not district:
        return DEFAULT_SHOPS
    return SAMPLE_AGRI_SHOPS.get(district, DEFAULT_SHOPS)
