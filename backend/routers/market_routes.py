import os
import random
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models, auth

router = APIRouter(prefix="/api/market", tags=["Market"])

# data.gov.in's "Variety-wise Daily Market Prices" resource (Agmarknet-sourced).
# Get a free API key at https://data.gov.in/user/register, then set:
#   DATA_GOV_API_KEY=your_key   in backend/.env
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "").strip()
DATA_GOV_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
DATA_GOV_URL = f"https://api.data.gov.in/resource/{DATA_GOV_RESOURCE_ID}"

# Fallback sample data used whenever DATA_GOV_API_KEY isn't configured, or
# the live API call fails -- keeps the Market page usable out of the box.
MOCK_PRICES = [
    {"crop": "Tomato", "market": "Nanded APMC", "price_per_quintal": 1450, "trend": "up", "change_pct": 4.2},
    {"crop": "Potato", "market": "Nanded APMC", "price_per_quintal": 980, "trend": "down", "change_pct": -2.1},
    {"crop": "Onion", "market": "Nanded APMC", "price_per_quintal": 1620, "trend": "up", "change_pct": 6.5},
    {"crop": "Soybean", "market": "Nanded APMC", "price_per_quintal": 4300, "trend": "stable", "change_pct": 0.3},
    {"crop": "Cotton", "market": "Nanded APMC", "price_per_quintal": 7200, "trend": "up", "change_pct": 3.1},
    {"crop": "Jowar", "market": "Nanded APMC", "price_per_quintal": 2650, "trend": "down", "change_pct": -1.4},
    {"crop": "Turmeric", "market": "Nanded APMC", "price_per_quintal": 8900, "trend": "up", "change_pct": 5.0},
]


def _mock_prices_for_district(district: str):
    market_name = f"{district} APMC" if district else "Nearest APMC"
    rng = random.Random(district or "default")
    results = []
    for row in MOCK_PRICES:
        jitter = rng.uniform(-40, 40)
        results.append({**row, "market": market_name, "price_per_quintal": round(row["price_per_quintal"] + jitter)})
    return results


def _fetch_live_prices(district: str):
    """Calls the data.gov.in Agmarknet-sourced resource, filtered by district.
    Returns None on any failure so the caller can fall back to mock data."""
    if not DATA_GOV_API_KEY:
        return None
    try:
        params = {"api-key": DATA_GOV_API_KEY, "format": "json", "limit": 20}
        if district:
            params["filters[district]"] = district
        res = requests.get(DATA_GOV_URL, params=params, timeout=10)
        res.raise_for_status()
        records = res.json().get("records", [])
        if not records:
            return None

        results = []
        for r in records:
            try:
                modal_price = float(r.get("modal_price", 0))
                min_price = float(r.get("min_price", modal_price))
                change_pct = round(((modal_price - min_price) / min_price) * 100, 1) if min_price else 0
                trend = "up" if change_pct > 1 else "down" if change_pct < -1 else "stable"
                results.append({
                    "crop": r.get("commodity", "Unknown"),
                    "market": r.get("market", district or "Unknown"),
                    "price_per_quintal": round(modal_price),
                    "trend": trend,
                    "change_pct": change_pct,
                })
            except (ValueError, TypeError):
                continue
        return results or None
    except requests.RequestException:
        return None


@router.get("/prices")
def get_prices(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    profile = db.query(models.FarmProfile).filter(models.FarmProfile.user_id == current_user.id).first()
    district = profile.district if profile else None

    live = _fetch_live_prices(district)
    if live:
        return {"source": "live", "district": district, "prices": live}

    return {"source": "sample", "district": district, "prices": _mock_prices_for_district(district)}


@router.get("/prices/trend")
def get_price_trend(crop: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """7-day price trend for a single crop. Uses sample data unless a live
    time-series source is configured (data.gov.in's daily resource only
    returns the latest snapshot per call, so a real 7-day series would need
    7 date-filtered calls or a scheduled ingestion job -- left as a hook)."""
    rng = random.Random(crop)
    base = rng.uniform(1000, 5000)
    today = datetime.utcnow().date()
    series = []
    price = base
    for i in range(6, -1, -1):
        price += rng.uniform(-80, 90)
        series.append({"date": str(today - timedelta(days=i)), "price": round(price)})
    return {"crop": crop, "series": series}
