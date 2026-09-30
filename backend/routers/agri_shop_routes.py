from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models, auth
from ml.agri_shops import get_shops_for_district

router = APIRouter(prefix="/api/agri-shops", tags=["Agri Shops"])


@router.get("/nearby")
def nearby_shops(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    profile = db.query(models.FarmProfile).filter(models.FarmProfile.user_id == current_user.id).first()
    district = profile.district if profile else None
    return {"district": district, "shops": get_shops_for_district(district)}
