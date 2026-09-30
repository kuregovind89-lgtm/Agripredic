"""
Land-area based pesticide/fungicide dosage & cost estimator.

IMPORTANT SAFETY NOTE: These are *general planning estimates* only, based on
standard agronomy spray-volume conventions (approx. 200 L of spray solution
per acre for field/row crops) and typical label dose ranges per severity
tier. They are NOT a substitute for the actual product label rate, which
varies by brand/formulation/concentration. Always confirm exact dosage
against the specific product's label or a local Krishi Seva Kendra /
agriculture extension officer before mixing or applying.
"""

STANDARD_SPRAY_VOLUME_L_PER_ACRE = 200  # typical for field & row vegetable crops

# General dose-per-litre-of-spray-solution ranges by severity, used only to
# produce a rough planning estimate (ml of concentrate per litre of water).
DOSE_ML_PER_L_BY_SEVERITY = {
    "Low": (1.0, 1.5),
    "Medium": (1.5, 2.5),
    "High": (2.5, 3.5),
}

# Rough per-acre cost bands (INR) for planning purposes only -- actual prices
# vary by brand, region, and season.
CHEMICAL_COST_PER_ACRE_INR = {"Low": (350, 600), "Medium": (600, 1000), "High": (1000, 1600)}
ORGANIC_COST_PER_ACRE_INR = {"Low": (250, 450), "Medium": (450, 750), "High": (750, 1200)}


def estimate_dosage(land_area_acres: float, severity: str):
    if not land_area_acres or land_area_acres <= 0:
        return None

    severity = severity if severity in DOSE_ML_PER_L_BY_SEVERITY else "Medium"
    total_spray_l = round(land_area_acres * STANDARD_SPRAY_VOLUME_L_PER_ACRE, 1)

    dose_lo, dose_hi = DOSE_ML_PER_L_BY_SEVERITY[severity]
    total_chemical_ml_lo = round(total_spray_l * dose_lo, 0)
    total_chemical_ml_hi = round(total_spray_l * dose_hi, 0)

    chem_cost_lo, chem_cost_hi = CHEMICAL_COST_PER_ACRE_INR[severity]
    org_cost_lo, org_cost_hi = ORGANIC_COST_PER_ACRE_INR[severity]

    return {
        "land_area_acres": land_area_acres,
        "spray_volume_liters": total_spray_l,
        "estimated_chemical_ml_range": f"{int(total_chemical_ml_lo)}-{int(total_chemical_ml_hi)} ml",
        "estimated_chemical_cost_inr": f"₹{int(land_area_acres * chem_cost_lo)}-{int(land_area_acres * chem_cost_hi)}",
        "estimated_organic_cost_inr": f"₹{int(land_area_acres * org_cost_lo)}-{int(land_area_acres * org_cost_hi)}",
        "disclaimer": (
            "General planning estimate based on standard spray-volume conventions (200 L/acre) "
            "and severity tier. Always confirm exact dosage against the product label or your "
            "local Krishi Seva Kendra / agriculture extension officer before mixing or applying."
        ),
        "disclaimer_mr": (
            "हे केवळ सर्वसाधारण अंदाजित मार्गदर्शन आहे (200 लिटर/एकर या प्रमाणित फवारणी आकारमानावर आधारित). "
            "प्रत्यक्ष फवारणी करण्यापूर्वी नेहमी उत्पादनाच्या लेबलवरील प्रमाण किंवा जवळच्या कृषी सेवा केंद्र/कृषी अधिकाऱ्याकडून खात्री करा."
        ),
    }
