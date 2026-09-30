from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/farm-profile", tags=["Farm Profile"])


@router.get("/", response_model=schemas.FarmProfileOut)
def get_profile(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    profile = db.query(models.FarmProfile).filter(models.FarmProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.FarmProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.put("/", response_model=schemas.FarmProfileOut)
def update_profile(
    payload: schemas.FarmProfileIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    profile = db.query(models.FarmProfile).filter(models.FarmProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.FarmProfile(user_id=current_user.id)
        db.add(profile)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
