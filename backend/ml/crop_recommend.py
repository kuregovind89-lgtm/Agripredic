"""
Crop recommendation engine.

Trains a scikit-learn RandomForestClassifier on a synthetic-but-agronomically
-grounded dataset generated from CROP_PROFILES (ml/crop_data.py) the first
time this module is imported, then keeps the fitted model in memory for the
life of the server process (training takes well under a second on this
small dataset, so no need to persist it to disk).

For production-grade accuracy, swap `_build_training_data()` to load the
real public "Crop Recommendation Dataset" (N, P, K, temperature, humidity,
ph, rainfall, label columns) instead of sampling from CROP_PROFILES.
"""
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from ml.crop_data import CROP_PROFILES

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

_model = None
_label_encoder = None


def _sample_profile(profile, rng):
    return [
        rng.uniform(*profile["N"]),
        rng.uniform(*profile["P"]),
        rng.uniform(*profile["K"]),
        rng.uniform(*profile["temp"]),
        rng.uniform(*profile["humidity"]),
        rng.uniform(*profile["ph"]),
        rng.uniform(*profile["rainfall"]),
    ]


def _build_training_data(samples_per_crop=120, seed=42):
    rng = random.Random(seed)
    X, y = [], []
    for crop, profile in CROP_PROFILES.items():
        for _ in range(samples_per_crop):
            X.append(_sample_profile(profile, rng))
            y.append(crop)
    return np.array(X), np.array(y)


def _get_model():
    global _model, _label_encoder
    if _model is not None:
        return _model, _label_encoder

    X, y = _build_training_data()
    _label_encoder = LabelEncoder()
    y_enc = _label_encoder.fit_transform(y)

    _model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    _model.fit(X, y_enc)
    return _model, _label_encoder


def recommend_crops(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall,
                     season=None, soil_type=None, top_n=3):
    model, encoder = _get_model()
    x = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
    proba = model.predict_proba(x)[0]

    ranked = sorted(zip(encoder.classes_, proba), key=lambda p: p[1], reverse=True)

    results = []
    for crop, prob in ranked:
        profile = CROP_PROFILES[crop]
        season_match = season is None or season in profile["seasons"]
        soil_match = soil_type is None or soil_type in profile["soils"]

        # Boost/penalize the raw ML probability using season & soil compatibility,
        # since the base classifier only sees numeric nutrient/climate features.
        adjusted = prob
        if season is not None:
            adjusted *= 1.25 if season_match else 0.55
        if soil_type is not None:
            adjusted *= 1.15 if soil_match else 0.7

        results.append({
            "crop": str(crop),
            "confidence": round(float(min(adjusted, 1.0) * 100), 2),
            "season_match": season_match,
            "soil_match": soil_match,
            "suitable_seasons": profile["seasons"],
            "suitable_soils": profile["soils"],
        })

    results.sort(key=lambda r: r["confidence"], reverse=True)
    return results[:top_n]
