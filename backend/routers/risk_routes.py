from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas, auth
from ml.risk_engine import assess_all_risks
from utils_weather import fetch_current_weather
from alerts import send_risk_alert

router = APIRouter(prefix="/api/risk", tags=["Risk Prediction"])


@router.get("/assess")
def assess(
    location: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    weather = fetch_current_weather(location)
    risks = assess_all_risks(
        temperature=weather["temperature"], humidity=weather["humidity"],
        rainfall=weather["rainfall"], wind_speed=weather["wind_speed"],
    )

    record = models.RiskAssessment(
        user_id=current_user.id, location=location,
        disease_risk=risks["disease_risk"], pest_risk=risks["pest_risk"],
        flood_risk=risks["flood_risk"], drought_risk=risks["drought_risk"],
        heatwave_risk=risks["heatwave_risk"], crop_failure_risk=risks["crop_failure_risk"],
        overall_level=risks["overall_level"],
    )
    db.add(record)
    db.commit()

    if risks["overall_level"] == "High":
        top_risk = max(
            [("Disease", risks["disease_risk"]), ("Pest", risks["pest_risk"]), ("Flood", risks["flood_risk"]),
             ("Drought", risks["drought_risk"]), ("Heatwave", risks["heatwave_risk"])],
            key=lambda p: p[1],
        )
        db.add(models.Notification(
            user_id=current_user.id, type="alert", title=f"High {top_risk[0]} Risk in {location}",
            message=f"Current conditions indicate a {top_risk[1]}% {top_risk[0].lower()} risk in {location}. Take preventive action.",
        ))
        db.commit()
        send_risk_alert(current_user, location, top_risk[0], top_risk[1])

    return {"location": location, "weather": weather, **risks}


@router.get("/history", response_model=List[schemas.RiskAssessmentOut])
def history(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return (
        db.query(models.RiskAssessment)
        .filter(models.RiskAssessment.user_id == current_user.id)
        .order_by(models.RiskAssessment.created_at.desc())
        .limit(20)
        .all()
    )
