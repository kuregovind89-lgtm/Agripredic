import csv
import io
import os
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from database import get_db
import models, auth

router = APIRouter(prefix="/api/reports", tags=["Reports"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")


def _pdf_response(title, current_user, rows, columns, filename):
    path = os.path.join(UPLOAD_DIR, filename)
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"AgriPredic - {title}")
    c.setFont("Helvetica", 10)
    c.drawString(50, 782, f"Farmer: {current_user.name}   |   Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    y = 750
    c.setFont("Helvetica-Bold", 10)
    header = "   ".join(columns)
    c.drawString(50, y, header[:110])
    y -= 18
    c.setFont("Helvetica", 9)
    for row in rows:
        line = "   ".join(str(row.get(col, ""))[:20] for col in columns)
        c.drawString(50, y, line[:115])
        y -= 16
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 9)
            y = 800
    c.save()
    return FileResponse(path, filename=filename)


def _csv_response(rows, columns, filename):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=columns)
    writer.writeheader()
    for row in rows:
        writer.writerow({col: row.get(col, "") for col in columns})
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]), media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/disease")
def disease_report(
    format: str = Query("pdf", pattern="^(pdf|csv)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    preds = (
        db.query(models.Prediction)
        .filter(models.Prediction.user_id == current_user.id)
        .order_by(models.Prediction.created_at.desc())
        .all()
    )
    columns = ["created_at", "crop", "disease_name", "confidence", "severity"]
    rows = [{
        "created_at": p.created_at.strftime("%Y-%m-%d"), "crop": p.crop,
        "disease_name": p.disease_name, "confidence": f"{p.confidence}%", "severity": p.severity,
    } for p in preds]

    if format == "csv":
        return _csv_response(rows, columns, "disease_report.csv")
    return _pdf_response("Disease Detection Report", current_user, rows, columns, "disease_report.pdf")


@router.get("/risk")
def risk_report(
    format: str = Query("pdf", pattern="^(pdf|csv)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    risks = (
        db.query(models.RiskAssessment)
        .filter(models.RiskAssessment.user_id == current_user.id)
        .order_by(models.RiskAssessment.created_at.desc())
        .all()
    )
    columns = ["created_at", "location", "disease_risk", "flood_risk", "drought_risk", "heatwave_risk", "overall_level"]
    rows = [{
        "created_at": r.created_at.strftime("%Y-%m-%d"), "location": r.location,
        "disease_risk": f"{r.disease_risk}%", "flood_risk": f"{r.flood_risk}%",
        "drought_risk": f"{r.drought_risk}%", "heatwave_risk": f"{r.heatwave_risk}%",
        "overall_level": r.overall_level,
    } for r in risks]

    if format == "csv":
        return _csv_response(rows, columns, "risk_report.csv")
    return _pdf_response("Risk Assessment Report", current_user, rows, columns, "risk_report.pdf")


@router.get("/farm")
def farm_report(
    format: str = Query("pdf", pattern="^(pdf|csv)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    profile = db.query(models.FarmProfile).filter(models.FarmProfile.user_id == current_user.id).first()
    pred_count = db.query(models.Prediction).filter(models.Prediction.user_id == current_user.id).count()
    high_risk_count = db.query(models.RiskAssessment).filter(
        models.RiskAssessment.user_id == current_user.id, models.RiskAssessment.overall_level == "High"
    ).count()

    columns = ["field", "value"]
    rows = [
        {"field": "Farm Name", "value": profile.farm_name if profile else "-"},
        {"field": "Land Area (acres)", "value": profile.land_area_acres if profile else "-"},
        {"field": "Soil Type", "value": profile.soil_type if profile else "-"},
        {"field": "Soil pH", "value": profile.soil_ph if profile else "-"},
        {"field": "Irrigation Source", "value": profile.irrigation_source if profile else "-"},
        {"field": "District", "value": profile.district if profile else "-"},
        {"field": "State", "value": profile.state if profile else "-"},
        {"field": "Total Disease Scans", "value": pred_count},
        {"field": "High-Risk Alerts Recorded", "value": high_risk_count},
    ]

    if format == "csv":
        return _csv_response(rows, columns, "farm_report.csv")
    return _pdf_response("Farm Summary Report", current_user, rows, columns, "farm_report.pdf")
