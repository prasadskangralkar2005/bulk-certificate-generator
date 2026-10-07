from pathlib import Path

from app.services.certificate_generator import generate_certificate


def test_generate_certificate(tmp_path, monkeypatch):
    # Use a temporary directory instead of the real
    # generated_certificates folder.
    monkeypatch.setattr(
        "app.services.certificate_generator.OUTPUT_DIR",
        tmp_path
    )

    file_path = generate_certificate(
        certificate_id=100,
        recipient_name="Prasad Kangralkar",
        event_name="Python Workshop",
        event_date="2026-10-07"
    )

    path = Path(file_path)

    assert path.exists()
    assert path.suffix == ".pdf"
    assert path.name == "certificate_100.pdf"
    assert path.stat().st_size > 0


def test_certificate_file_is_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.services.certificate_generator.OUTPUT_DIR",
        tmp_path
    )

    file_path = generate_certificate(
        certificate_id=101,
        recipient_name="Rahul Sharma",
        event_name="AI Workshop",
        event_date="2026-10-07"
    )

    path = Path(file_path)

    with open(path, "rb") as pdf_file:
        header = pdf_file.read(4)

    assert header == b"%PDF"