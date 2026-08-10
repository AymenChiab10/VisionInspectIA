"""
Logique metier de la prediction (upload + inference + enregistrement).

Ce module concentre toute la logique : validation du fichier, sauvegarde
sur disque, appel au preprocessing, appel au modele, puis enregistrement
du resultat dans la table 'inspections'. La route associee ne fait
qu'appeler predict_image().
"""

import time
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.ml.model_loader import model_loader
from app.ml.preprocessing import preprocess_image
from app.models.inspection import Inspection
from app.models.user import User
from app.utils.file_utils import generate_unique_filename, validate_image_file

# backend/app/services/prediction_service.py -> backend/uploads
UPLOADS_DIR = Path(__file__).resolve().parents[2] / "uploads"


def predict_image(
    db: Session,
    current_user: User,
    filename: str,
    content: bytes,
) -> tuple[Inspection, float]:
    """
    Traite une image uploadee de bout en bout :
    1. valide le fichier (extension, taille) ;
    2. le pretraite (rejette une image corrompue avant d'ecrire quoi que ce soit) ;
    3. le sauvegarde dans uploads/ sous un nom unique ;
    4. l'envoie au modele MobileNetV2 (duree mesuree) ;
    5. enregistre le resultat dans la table 'inspections' (nettoie le fichier
       si l'enregistrement en base echoue, pour ne jamais laisser de fichier
       orphelin sur le disque).

    Retourne un tuple (Inspection creee, duree d'inference en millisecondes).
    La duree n'est pas persistee en base (uniquement affichee au frontend),
    donc aucun changement du modele SQLAlchemy Inspection n'est necessaire.
    """
    validate_image_file(filename, content)

    try:
        image_tensor = preprocess_image(content)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image invalide ou corrompue.",
        )

    unique_filename = generate_unique_filename(filename)
    destination = UPLOADS_DIR / unique_filename
    destination.write_bytes(content)

    inference_start = time.perf_counter()
    predicted_class, confidence = model_loader.predict(image_tensor)
    inference_time_ms = (time.perf_counter() - inference_start) * 1000

    inspection = Inspection(
        image_path=f"uploads/{unique_filename}",
        predicted_class=predicted_class,
        confidence=confidence,
        user_id=current_user.id,
    )

    try:
        db.add(inspection)
        db.commit()
        db.refresh(inspection)
    except Exception:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise

    return inspection, inference_time_ms
