from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    location = Column(String(150), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="farmer")  # farmer | admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    predictions = relationship("Prediction", back_populates="owner")


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    crop = Column(String(100), nullable=False)
    severity_default = Column(String(20), default="Medium")  # Low/Medium/High
    treatment = Column(Text, nullable=True)
    fertilizer = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String(255), nullable=False)
    disease_name = Column(String(150), nullable=False)
    disease_name_mr = Column(String(150), nullable=True)
    crop = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    treatment = Column(Text, nullable=True)
    fertilizer = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    treatment_mr = Column(Text, nullable=True)
    fertilizer_mr = Column(Text, nullable=True)
    prevention_mr = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="predictions")


class WeatherRisk(Base):
    __tablename__ = "weather_risk"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String(150), nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    risk_level = Column(String(20), nullable=False)
    risk_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(30), default="alert")  # alert | info
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FarmProfile(Base):
    __tablename__ = "farm_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    farm_name = Column(String(150), nullable=True)
    land_area_acres = Column(Float, nullable=True)
    soil_type = Column(String(50), nullable=True)
    soil_ph = Column(Float, nullable=True)
    irrigation_source = Column(String(50), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    primary_crop = Column(String(100), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    soil_type = Column(String(50), nullable=True)
    soil_ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    season = Column(String(30), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    top_crop = Column(String(100), nullable=False)
    top_confidence = Column(Float, nullable=False)
    results_json = Column(Text, nullable=False)  # top-3 recommendations serialized
    created_at = Column(DateTime, default=datetime.utcnow)


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String(150), nullable=False)
    disease_risk = Column(Float, nullable=False)
    pest_risk = Column(Float, nullable=False)
    flood_risk = Column(Float, nullable=False)
    drought_risk = Column(Float, nullable=False)
    heatwave_risk = Column(Float, nullable=False)
    crop_failure_risk = Column(Float, nullable=False)
    overall_level = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
