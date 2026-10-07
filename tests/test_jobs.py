def test_create_job(client):
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Prasad Kangralkar",
                "email": "prasad@example.com"
            },
            {
                "name": "Rahul Sharma",
                "email": "rahul@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=payload)

    # Job creation is asynchronous.
    assert response.status_code == 202

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "queued"
    assert data["total_count"] == 2
    assert data["message"] == "Bulk certificate generation job created"


def test_get_job_status(client):
    payload = {
        "event_name": "AI Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Prasad Kangralkar",
                "email": "prasad@example.com"
            }
        ]
    }

    create_response = client.post("/jobs", json=payload)

    assert create_response.status_code == 202

    job_id = create_response.json()["job_id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["total_count"] == 1
    assert data["status"] in [
        "queued",
        "running",
        "completed",
        "partial",
        "failed"
    ]


def test_get_nonexistent_job(client):
    response = client.get("/jobs/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Job not found"