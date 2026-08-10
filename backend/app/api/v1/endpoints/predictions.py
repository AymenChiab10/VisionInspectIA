"""
Routes de prediction (upload d'image + inference IA).

Aucune logique metier ici : la route delegue entierement a
app/services/prediction_service.py.
"""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services import prediction_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Endpoint de test confirmant que le module predictions est charge."""
    return {"module": "predictions", "status": "ready"}


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Recoit une image, effectue une prediction MobileNetV2 et l'enregistre."""
    content = await file.read()

    inspection, inference_time_ms = prediction_service.predict_image(
        db=db,
        current_user=current_user,
        filename=file.filename,
        content=content,
    )

    return {
        "predicted_class": inspection.predicted_class,
        "confidence": inspection.confidence,
        "image_path": inspection.image_path,
        "created_at": inspection.created_at,
        "inference_time_ms": round(inference_time_ms, 2),
    }
