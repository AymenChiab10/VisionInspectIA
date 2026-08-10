"""
Generation de rapports PDF (Partie rapports).

Construit un PDF simple, entierement en memoire (aucun fichier temporaire
ecrit sur disque), a partir d'une inspection et de l'utilisateur associe.
Utilise uniquement ReportLab.
"""

from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer

from app.models.inspection import Inspection
from app.models.user import User

# backend/app/utils/pdf_utils.py -> backend/
BACKEND_ROOT = Path(__file__).resolve().parents[2]


def generate_pdf(inspection: Inspection, user: User) -> BytesIO:
    """
    Genere le rapport PDF d'une inspection.

    Retourne un buffer BytesIO positionne au debut, contenant le PDF.
    Aucun fichier n'est ecrit sur disque.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    confidence_percent = inspection.confidence * 100

    elements = []

    # --- Titre ---
    elements.append(Paragraph("Bottle Defect Detection Report", styles["Title"]))
    elements.append(Spacer(1, 1 * cm))

    # --- Informations utilisateur ---
    elements.append(Paragraph("User Information", styles["Heading2"]))
    elements.append(Paragraph(f"First name: {user.first_name}", styles["Normal"]))
    elements.append(Paragraph(f"Last name: {user.last_name}", styles["Normal"]))
    elements.append(Paragraph(f"Email: {user.email}", styles["Normal"]))
    elements.append(Spacer(1, 0.6 * cm))

    # --- Informations inspection ---
    elements.append(Paragraph("Inspection Information", styles["Heading2"]))
    elements.append(Paragraph(f"ID: {inspection.id}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {inspection.created_at}", styles["Normal"]))
    elements.append(Paragraph(f"Predicted class: {inspection.predicted_class}", styles["Normal"]))
    elements.append(Paragraph(f"Confidence: {confidence_percent:.2f} %", styles["Normal"]))
    elements.append(Spacer(1, 0.6 * cm))

    # --- Image inspectee ---
    image_path = BACKEND_ROOT / inspection.image_path
    if image_path.exists():
        elements.append(Paragraph("Inspected Image", styles["Heading2"]))
        elements.append(Image(str(image_path), width=8 * cm, height=8 * cm))
        elements.append(Spacer(1, 0.6 * cm))

    # --- Conclusion ---
    elements.append(Paragraph("Conclusion", styles["Heading2"]))
    elements.append(Paragraph("Inspection completed successfully.", styles["Normal"]))
    elements.append(Paragraph(f"Predicted class: {inspection.predicted_class.upper()}", styles["Normal"]))
    elements.append(Paragraph(f"Confidence: {confidence_percent:.2f} %", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer
