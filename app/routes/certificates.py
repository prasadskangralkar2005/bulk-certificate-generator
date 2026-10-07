from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Certificate, Job


router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"]
)


@router.get("/job/{job_id}")
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all successfully generated certificates
    belonging to a job.
    """

    # Check that the job exists
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    certificates = (
        db.query(Certificate)
        .join(
            Certificate.recipient
        )
        .filter(
            Certificate.recipient.has(
                job_id=job_id
            )
        )
        .all()
    )

    return {
        "job_id": job_id,
        "certificate_count": len(certificates),
        "certificates": [
            {
                "certificate_id": certificate.id,
                "recipient_id": certificate.recipient_id,
                "file_path": certificate.file_path
            }
            for certificate in certificates
        ]
    }


@router.get("/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    """
    Download a generated certificate PDF.
    """

    certificate = (
        db.query(Certificate)
        .filter(
            Certificate.id == certificate_id
        )
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    file_path = Path(certificate.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_path.name
    )