# Bulk Certificate Generator Backend

A Python-based REST API for generating participation certificates in bulk.

The system accepts a single bulk request containing event information and multiple recipients. It creates a background job, generates an individual PDF certificate for each recipient, tracks job progress, stores certificate information in a relational database, and provides APIs to retrieve and download generated certificates.

---

## Features

- Bulk certificate generation
- Multiple recipients in a single request
- Input validation using Pydantic
- Asynchronous/background processing
- Job status tracking
- Real-time progress calculation
- Individual recipient failure handling
- Failure isolation so one failed certificate does not stop the complete job
- PDF certificate generation
- SQLite relational database
- Certificate retrieval by job
- Individual certificate download
- Automated tests using pytest
- Interactive API documentation using Swagger UI

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Request validation |
| SQLAlchemy | ORM and database interaction |
| SQLite | Relational database |
| ReportLab | PDF certificate generation |
| pytest | Automated testing |
| Uvicorn | ASGI server |

---

## System Architecture

```text
Client
  |
  | POST /jobs
  v
FastAPI API
  |
  | Validate request
  v
Create Job + Recipients
  |
  | 202 Accepted
  v
Background Processing
  |
  +----------------------+
  |                      |
  v                      v
Recipient 1          Recipient N
  |                      |
  v                      v
Generate PDF         Generate PDF
  |                      |
  +----------+-----------+
             |
             v
        SQLite Database
             |
             v
       Job Status / Progress
             |
             v
     Certificate Retrieval
             |
             v
       PDF Download