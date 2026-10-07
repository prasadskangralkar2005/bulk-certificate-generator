def test_get_job_certificates(client):
    payload = {
        "event_name": "Python Workshop",
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

    response = client.get(f"/certificates/job/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert "certificate_count" in data
    assert "certificates" in data


def test_get_certificates_for_nonexistent_job(client):
    response = client.get("/certificates/job/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Job not found"


def test_download_nonexistent_certificate(client):
    response = client.get("/certificates/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Certificate not found"