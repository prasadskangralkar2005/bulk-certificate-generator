from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import SessionLocal, get_db
from ..models import Job, Recipient, Certificate
from ..schemas import JobCreate
from ..services.certificate_generator import generate_certificate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


def process_job(job_id: int):
    """
    Process all recipients belonging to a job.

    Each recipient is processed independently.
    If one certificate fails, the remaining recipients continue processing.
    """

    db = SessionLocal()

    try:
        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if not job:
            return

        job.status = "running"
        job.started_at = datetime.utcnow()
        db.commit()

        recipients = (
            db.query(Recipient)
            .filter(Recipient.job_id == job_id)
            .all()
        )

        for recipient in recipients:

            # Skip recipients that have already completed.
            if recipient.status == "completed":
                continue

            try:
                recipient.status = "processing"
                db.commit()

                certificate_path = generate_certificate(
                    certificate_id=recipient.id,
                    recipient_name=recipient.name,
                    event_name=job.event_name,
                    event_date=job.event_date
                )

                certificate = Certificate(
                    recipient_id=recipient.id,
                    file_path=certificate_path
                )

                db.add(certificate)

                recipient.status = "completed"
                recipient.error_message = None

                job.success_count += 1

                db.commit()

            except Exception as error:
                # Roll back any incomplete database transaction.
                db.rollback()

                # Mark only this recipient as failed.
                recipient.status = "failed"
                recipient.error_message = str(error)

                job.failed_count += 1

                db.commit()

                # Continue with the next recipient.
                continue

        # Determine final job status.
        if job.failed_count == 0:
            job.status = "completed"

        elif job.success_count == 0:
            job.status = "failed"

        else:
            job.status = "partial"

        job.completed_at = datetime.utcnow()

        db.commit()

    except Exception:
        # Handle unexpected job-level failures.
        db.rollback()

        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if job:
            job.status = "failed"
            job.completed_at = datetime.utcnow()
            db.commit()

    finally:
        db.close()


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED
)
def create_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a bulk certificate generation job.

    The request is accepted immediately and certificate generation
    continues in the background.
    """

    job = Job(
        event_name=job_data.event_name,
        event_date=job_data.event_date.isoformat(),
        total_count=len(job_data.recipients),
        success_count=0,
        failed_count=0,
        status="queued"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient_data in job_data.recipients:

        recipient = Recipient(
            job_id=job.id,
            name=recipient_data.name,
            email=recipient_data.email,
            status="pending"
        )

        db.add(recipient)

    db.commit()

    background_tasks.add_task(
        process_job,
        job.id
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count,
        "message": "Bulk certificate generation job created"
    }


@router.get("/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the current status and progress of a job.
    """

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    progress = 0

    if job.total_count > 0:
        progress = round(
            (
                (job.success_count + job.failed_count)
                / job.total_count
            ) * 100
        )

    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count,
        "success_count": job.success_count,
        "failed_count": job.failed_count,
        "progress": progress,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at
    }