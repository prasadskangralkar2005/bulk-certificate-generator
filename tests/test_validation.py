def test_valid_job_data(client):
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

    response = client.post("/jobs", json=payload)

    assert response.status_code == 202

    data = response.json()

    assert "job_id" in data
    assert data["total_count"] == 1


def test_invalid_email(client):
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Prasad Kangralkar",
                "email": "invalid-email"
            }
        ]
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 422


def test_empty_recipient_list(client):
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-07",
        "recipients": []
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 422


def test_short_recipient_name(client):
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "A",
                "email": "a@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 422


def test_missing_event_name(client):
    payload = {
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Prasad Kangralkar",
                "email": "prasad@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 422