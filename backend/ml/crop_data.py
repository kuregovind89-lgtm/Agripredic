"""
Agronomic reference profiles for common crops grown in India, giving typical
suitable ranges for soil nutrients (N-P-K, kg/ha), pH, temperature (°C),
humidity (%), and rainfall (mm). Ranges are drawn from general agronomy
reference values (similar in structure to the well-known public "Crop
Recommendation Dataset") and are used to generate a synthetic-but-realistic
training set for the crop recommendation model in crop_recommend.py.

NOTE: For maximum real-world accuracy, replace this synthetic generator
with the actual Kaggle "Crop Recommendation Dataset" (~2200 real records)
by loading it as a CSV in crop_recommend.py -- the training code already
expects the same column layout (N, P, K, temperature, humidity, ph,
rainfall, label), so this is a drop-in swap.
"""

CROP_PROFILES = {
    "Rice":       {"N": (60, 100), "P": (30, 60), "K": (30, 60), "temp": (20, 32), "humidity": (70, 90), "ph": (5.5, 7.0), "rainfall": (150, 300), "seasons": ["Kharif"], "soils": ["Clay", "Loamy", "Alluvial"]},
    "Wheat":      {"N": (80, 120), "P": (40, 60), "K": (30, 50), "temp": (10, 25), "humidity": (50, 70), "ph": (6.0, 7.5), "rainfall": (50, 100), "seasons": ["Rabi"], "soils": ["Loamy", "Clay", "Alluvial"]},
    "Maize":      {"N": (70, 110), "P": (35, 60), "K": (25, 50), "temp": (18, 30), "humidity": (55, 75), "ph": (5.8, 7.2), "rainfall": (60, 120), "seasons": ["Kharif", "Rabi"], "soils": ["Loamy", "Sandy Loam"]},
    "Cotton":     {"N": (100, 140), "P": (40, 60), "K": (40, 60), "temp": (22, 35), "humidity": (40, 65), "ph": (6.0, 8.0), "rainfall": (60, 110), "seasons": ["Kharif"], "soils": ["Black", "Loamy"]},
    "Sugarcane":  {"N": (150, 220), "P": (50, 80), "K": (60, 100), "temp": (21, 35), "humidity": (65, 85), "ph": (6.0, 7.5), "rainfall": (150, 250), "seasons": ["Kharif", "Annual"], "soils": ["Loamy", "Clay", "Alluvial"]},
    "Soybean":    {"N": (20, 40), "P": (40, 70), "K": (30, 50), "temp": (20, 30), "humidity": (60, 80), "ph": (6.0, 7.5), "rainfall": (90, 150), "seasons": ["Kharif"], "soils": ["Loamy", "Black"]},
    "Groundnut":  {"N": (15, 35), "P": (35, 55), "K": (35, 55), "temp": (22, 32), "humidity": (55, 75), "ph": (6.0, 7.0), "rainfall": (60, 120), "seasons": ["Kharif"], "soils": ["Sandy Loam", "Loamy"]},
    "Chickpea":   {"N": (15, 35), "P": (35, 55), "K": (15, 30), "temp": (15, 27), "humidity": (40, 60), "ph": (6.0, 7.5), "rainfall": (35, 65), "seasons": ["Rabi"], "soils": ["Loamy", "Clay", "Black"]},
    "Lentil":     {"N": (15, 30), "P": (30, 50), "K": (15, 30), "temp": (14, 25), "humidity": (40, 60), "ph": (6.0, 7.5), "rainfall": (35, 60), "seasons": ["Rabi"], "soils": ["Loamy", "Clay"]},
    "Onion":      {"N": (60, 100), "P": (40, 60), "K": (50, 80), "temp": (15, 28), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (60, 100), "seasons": ["Rabi", "Kharif"], "soils": ["Loamy", "Sandy Loam"]},
    "Tomato":     {"N": (80, 120), "P": (50, 80), "K": (60, 100), "temp": (18, 29), "humidity": (55, 75), "ph": (6.0, 6.8), "rainfall": (60, 130), "seasons": ["Rabi", "Kharif"], "soils": ["Loamy", "Sandy Loam"]},
    "Potato":     {"N": (100, 150), "P": (50, 80), "K": (100, 150), "temp": (15, 24), "humidity": (60, 80), "ph": (5.0, 6.5), "rainfall": (50, 100), "seasons": ["Rabi"], "soils": ["Loamy", "Sandy Loam"]},
    "Grapes":     {"N": (40, 70), "P": (30, 50), "K": (60, 100), "temp": (15, 35), "humidity": (40, 60), "ph": (6.5, 7.5), "rainfall": (50, 90), "seasons": ["Annual"], "soils": ["Loamy", "Black"]},
    "Banana":     {"N": (150, 220), "P": (50, 80), "K": (200, 300), "temp": (22, 32), "humidity": (70, 90), "ph": (6.0, 7.5), "rainfall": (120, 220), "seasons": ["Annual"], "soils": ["Loamy", "Alluvial"]},
    "Mango":      {"N": (40, 70), "P": (30, 50), "K": (40, 70), "temp": (24, 36), "humidity": (45, 65), "ph": (5.5, 7.5), "rainfall": (80, 150), "seasons": ["Annual"], "soils": ["Loamy", "Alluvial", "Laterite"]},
    "Jowar":      {"N": (60, 90), "P": (25, 45), "K": (20, 40), "temp": (25, 35), "humidity": (35, 55), "ph": (6.0, 7.8), "rainfall": (40, 90), "seasons": ["Kharif", "Rabi"], "soils": ["Black", "Loamy"]},
    "Bajra":      {"N": (40, 70), "P": (20, 40), "K": (15, 35), "temp": (25, 35), "humidity": (30, 50), "ph": (6.5, 8.0), "rainfall": (30, 70), "seasons": ["Kharif"], "soils": ["Sandy", "Sandy Loam"]},
    "Turmeric":   {"N": (60, 100), "P": (40, 60), "K": (60, 100), "temp": (20, 32), "humidity": (65, 85), "ph": (5.5, 7.0), "rainfall": (150, 230), "seasons": ["Kharif"], "soils": ["Loamy", "Clay"]},
}

SOIL_TYPES = ["Loamy", "Clay", "Sandy", "Sandy Loam", "Black", "Alluvial", "Laterite"]
SEASONS = ["Kharif", "Rabi", "Zaid", "Annual"]

# Typical N-P-K (kg/ha) and pH defaults per soil type, used to auto-fill the
# Crop Recommendation form when a farmer doesn't have a soil test report.
# These are general agronomy reference midpoints, not a substitute for an
# actual soil test -- encourage farmers to get one when possible.
SOIL_NPK_DEFAULTS = {
    "Loamy":       {"N": 80,  "P": 45, "K": 45,  "ph": 6.5},
    "Clay":        {"N": 70,  "P": 40, "K": 55,  "ph": 6.8},
    "Sandy":       {"N": 45,  "P": 25, "K": 25,  "ph": 6.2},
    "Sandy Loam":  {"N": 60,  "P": 35, "K": 35,  "ph": 6.3},
    "Black":       {"N": 90,  "P": 40, "K": 50,  "ph": 7.2},
    "Alluvial":    {"N": 85,  "P": 45, "K": 45,  "ph": 6.7},
    "Laterite":    {"N": 55,  "P": 30, "K": 35,  "ph": 5.8},
}
