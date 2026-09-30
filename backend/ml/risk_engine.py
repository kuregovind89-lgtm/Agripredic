"""
Multi-factor agricultural risk scoring engine.

Each risk is computed as a 0-100 score from live weather signals using
agronomy-based heuristics (documented inline), then mapped to Low/Medium/High.
This is a deterministic, explainable rule-based model -- not a black-box ML
model -- which is the right choice here since there's no labeled historical
outbreak/flood/drought dataset available to train a supervised model on.
"""


def _level(score):
    if score >= 65:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"


def _clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))


def assess_all_risks(temperature, humidity, rainfall, wind_speed=None):
    """temperature in °C, humidity in %, rainfall in mm (recent/daily), wind_speed in km/h."""
    temperature = temperature if temperature is not None else 25
    humidity = humidity if humidity is not None else 50
    rainfall = rainfall if rainfall is not None else 0
    wind_speed = wind_speed if wind_speed is not None else 10

    # Disease risk: fungal pathogens thrive in warm, humid, wet conditions
    disease = 0
    if humidity >= 80: disease += 40
    elif humidity >= 60: disease += 20
    if 20 <= temperature <= 30: disease += 30
    if rainfall > 5: disease += 30
    disease = _clamp(disease)

    # Pest risk: warm + moderately humid conditions favor insect breeding cycles
    pest = 0
    if 25 <= temperature <= 35: pest += 40
    if 40 <= humidity <= 70: pest += 30
    if rainfall < 2: pest += 20  # dry spells often precede aphid/mite outbreaks
    pest = _clamp(pest)

    # Flood risk: heavy rainfall accumulation
    if rainfall > 50: flood = 90
    elif rainfall > 20: flood = 60
    elif rainfall > 8: flood = 30
    else: flood = 5
    flood = _clamp(flood)

    # Drought risk: high heat, low humidity, little/no rain
    drought = 0
    if rainfall < 1: drought += 40
    if humidity < 35: drought += 30
    if temperature > 32: drought += 30
    drought = _clamp(drought)

    # Heatwave risk: absolute temperature thresholds
    if temperature >= 42: heatwave = 90
    elif temperature >= 38: heatwave = 65
    elif temperature >= 35: heatwave = 40
    else: heatwave = _clamp((temperature - 25) * 4)

    # Crop failure risk: weighted aggregate of the above, plus wind stress
    wind_factor = _clamp((wind_speed - 20) * 2) if wind_speed > 20 else 0
    crop_failure = _clamp(
        0.25 * flood + 0.25 * drought + 0.2 * disease + 0.15 * pest + 0.1 * heatwave + 0.05 * wind_factor
    )

    risks = {
        "disease_risk": round(disease, 1),
        "pest_risk": round(pest, 1),
        "flood_risk": round(flood, 1),
        "drought_risk": round(drought, 1),
        "heatwave_risk": round(heatwave, 1),
        "crop_failure_risk": round(crop_failure, 1),
    }
    levels = {f"{k}_level": _level(v) for k, v in risks.items()}

    overall_score = sum(risks.values()) / len(risks)
    overall_level = _level(overall_score)

    return {**risks, **levels, "overall_level": overall_level, "overall_score": round(overall_score, 1)}
