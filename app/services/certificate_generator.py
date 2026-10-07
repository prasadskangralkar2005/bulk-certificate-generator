from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    certificate_id: int,
    recipient_name: str,
    event_name: str,
    event_date: str
) -> str:
    """
    Generate a certificate PDF for one recipient.

    Returns:
        str: Path of the generated PDF.
    """

    filename = f"certificate_{certificate_id}.pdf"
    file_path = OUTPUT_DIR / filename

    width, height = landscape(A4)

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=(width, height)
    )

    # Outer border
    pdf.setStrokeColor(
        colors.HexColor("#1F4E79")
    )

    pdf.setLineWidth(4)

    pdf.rect(
        30,
        30,
        width - 60,
        height - 60
    )

    # Certificate title
    pdf.setFillColor(
        colors.HexColor("#1F4E79")
    )

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.drawCentredString(
        width / 2,
        height - 110,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Introduction
    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 155,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFillColor(
        colors.HexColor("#1F4E79")
    )

    pdf.setFont(
        "Helvetica-Bold",
        28
    )

    pdf.drawCentredString(
        width / 2,
        height - 215,
        recipient_name
    )

    # Event
    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 265,
        f"For successfully participating in {event_name}"
    )

    # Date
    pdf.setFont(
        "Helvetica",
        13
    )

    pdf.drawCentredString(
        width / 2,
        height - 315,
        f"Date: {event_date}"
    )

    # Footer
    pdf.setFont(
        "Helvetica-Oblique",
        11
    )

    pdf.drawCentredString(
        width / 2,
        75,
        "Bulk Certificate Generator"
    )

    pdf.save()

    return str(file_path)