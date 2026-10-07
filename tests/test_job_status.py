def test_job_status_for_new_job(client):
    payload = {
        "event_name": "Mechanical Engineering Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Prasad Kangralkar",
                "email": "prasad@example.com"
            },
            {
                "name": "Rahul Sharma",
                "email": "rahul@example.com"
            },
            {
                "name": "Amit Kumar",
                "email": "amit@example.com"
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
    assert data["total_count"] == 3

    assert data["success_count"] >= 0
    assert data["failed_count"] >= 0

    assert 0 <= data["progress"] <= 100

    assert data["status"] in [
        "queued",
        "running",
        "completed",
        "partial",
        "failed"
    ]


def test_job_progress_initially_valid(client):
    payload = {
        "event_name": "Testing Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Test User",
                "email": "test@example.com"
            }
        ]
    }

    create_response = client.post("/jobs", json=payload)

    assert create_response.status_code == 202

    job_id = create_response.json()["job_id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert 0 <= data["progress"] <= 100

    assert (
        data["success_count"] + data["failed_count"]
        <= data["total_count"]
    )


def test_job_contains_timestamps(client):
    payload = {
        "event_name": "Automation Workshop",
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

    assert data["created_at"] is not None