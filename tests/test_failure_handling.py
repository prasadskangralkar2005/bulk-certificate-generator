from app.database import SessionLocal
from app.models import Job, Recipient
from app.routes.jobs import process_job
import app.routes.jobs as jobs_module


def test_individual_certificate_failure_does_not_stop_job(
    monkeypatch,
    tmp_path
):
    db = SessionLocal()

    try:
        # Create a test job
        job = Job(
            event_name="Failure Test Event",
            event_date="2026-10-07",
            total_count=3,
            success_count=0,
            failed_count=0,
            status="queued"
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # Create three recipients
        recipients = [
            Recipient(
                job_id=job.id,
                name="Successful One",
                email="one@example.com",
                status="pending"
            ),
            Recipient(
                job_id=job.id,
                name="Failing One",
                email="two@example.com",
                status="pending"
            ),
            Recipient(
                job_id=job.id,
                name="Successful Two",
                email="three@example.com",
                status="pending"
            )
        ]

        db.add_all(recipients)
        db.commit()

        # Save original generator
        original_generator = jobs_module.generate_certificate

        def fake_generator(
            certificate_id,
            recipient_name,
            event_name,
            event_date
        ):
            if recipient_name == "Failing One":
                raise RuntimeError(
                    "Simulated certificate generation failure"
                )

            file_path = tmp_path / f"certificate_{certificate_id}.pdf"
            file_path.write_text("test certificate")

            return str(file_path)

        # Replace generator with our test version
        monkeypatch.setattr(
            jobs_module,
            "generate_certificate",
            fake_generator
        )

        # Process job
        process_job(job.id)

        # Refresh data
        db.expire_all()

        updated_job = (
            db.query(Job)
            .filter(Job.id == job.id)
            .first()
        )

        updated_recipients = (
            db.query(Recipient)
            .filter(Recipient.job_id == job.id)
            .order_by(Recipient.id)
            .all()
        )

        # Verify job status
        assert updated_job.status == "partial"

        assert updated_job.total_count == 3

        assert updated_job.success_count == 2

        assert updated_job.failed_count == 1

        # Verify individual statuses
        assert updated_recipients[0].status == "completed"

        assert updated_recipients[1].status == "failed"

        assert updated_recipients[2].status == "completed"

        # Verify error was recorded
        assert (
            updated_recipients[1].error_message
            == "Simulated certificate generation failure"
        )

    finally:
        db.close()