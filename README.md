# Digital Healthcare System

A full-stack Django web application for connecting patients and doctors online. Patients can register, browse doctors, book appointments, chat with an AI health assistant, and manage medical history. Doctors can maintain profiles, publish posts, confirm appointments, conduct video calls, and record diagnostic results.

Built as a digital health platform with role-based access control, advanced appointment scheduling, REST-style scheduling APIs, and automated test coverage enforced in CI.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Docker](#docker)
- [CI / Coverage](#ci--coverage)
- [Scheduling API](#scheduling-api)
- [Access Control](#access-control)
- [URL Overview](#url-overview)
- [Screenshots & Media](#screenshots--media)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Patients
- Sign up, log in, and manage a personal profile
- Browse and search doctors by specialization, region, and other filters
- Schedule, reschedule, edit, and cancel appointments
- View appointment history and join video calls
- Chat with a Google Gemini–powered AI assistant for general health guidance
- View medical history and diagnostic records added by doctors

### Doctors
- Register with email verification and admin approval workflow
- Complete profile with credentials, specialization, and verification documents
- Browse peer doctors and manage public posts (create, edit, delete)
- View, confirm, reschedule, and manage patient appointments
- Start video calls with patients
- Add diagnostic results and medical history entries for patients

### Appointments & Scheduling
- Web-based appointment booking with status workflow (`pending`, `accepted`, `declined`, `rescheduled`, `completed`)
- Advanced scheduling service with conflict detection and atomic slot booking
- JSON API for listing available slots and creating appointments programmatically
- Recurrence and exception fields on appointments for future recurring schedules

### Ratings
- Patients can rate doctors and leave written reviews
- Average ratings displayed on doctor profiles

### Platform & Security
- Centralized access-control policies (`access/policy.py`) with decorators for authenticated views
- Policy checks for creating, viewing, editing, and deleting appointments
- Django admin panel for managing users and content

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5.0 |
| Database | SQLite (development) |
| AI Assistant | Google Generative AI (Gemini) |
| Image handling | Pillow |
| Config | python-decouple, python-dotenv |
| Testing | pytest, pytest-cov |
| CI | GitHub Actions |
| Containerization | Docker (Python 3.11 slim) |

---

## Project Structure

```
Digital-healthcare-system/
├── Digitalhealthcare/       # Project settings, root URLs, homepage
├── patients/                # Patient auth, dashboard, AI chat, medical history
├── doctors/                 # Doctor registration, profiles, posts, browse
├── appointments/            # Scheduling views, API, scheduler service
├── rating/                  # Doctor ratings and reviews
├── adminpanel/              # Admin extensions
├── access/                  # Role detection, policies, auth decorators
├── static/                  # Collected static assets
├── media/                   # User-uploaded files (photos, documents)
├── .github/workflows/       # CI pipeline
├── Dockerfile
├── requirements.txt
├── .coveragerc
└── manage.py
```

---

## Prerequisites

- **Python 3.11+**
- **pip**
- (Optional) **Docker** for containerized runs
- (Optional) **Google API key** for Gemini AI chat
- (Optional) **SMTP credentials** for doctor email verification

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Samuel-K95/Digital-healthcare-system.git
cd Digital-healthcare-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov   # required for running the test suite locally
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

---

## Environment Variables

Create a `.env` file in the project root (or set variables in your environment). Email settings are loaded via `python-decouple` in `Digitalhealthcare/settings.py`.

| Variable | Description |
|----------|-------------|
| `EMAIL_HOST` | SMTP server hostname |
| `EMAIL_PORT` | SMTP port (integer) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `EMAIL_USE_TLS` | Enable TLS (`True` / `False`) |
| `DEFAULT_FROM_EMAIL` | Sender address for outgoing mail |
| `GOOGLE_API_KEY` | Google Generative AI API key for Gemini chat |

> **Note:** The Gemini module degrades gracefully when `GOOGLE_API_KEY` is missing or the SDK is unavailable—the rest of the application continues to work.

Example `.env`:

```env
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@example.com
GOOGLE_API_KEY=your-google-api-key
```

---

## Running the Application

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/admin/` | Django admin |
| `/Patients/` | Patient portal |
| `/Doctors/` | Doctor portal |
| `/Appointments/` | Appointment management |
| `/Rating/` | Doctor ratings |

Lowercase URL aliases (`/patients/`, `/doctors/`, `/appointments/`) are also supported for API integrations and tests.

---

## Running Tests

The project uses **pytest** with a **90% minimum coverage** threshold (matching CI).

```bash
pytest --maxfail=1 --disable-warnings -q --cov=. --cov-report=term-missing --cov-fail-under=90
```

Generate an HTML coverage report:

```bash
coverage html -d coverage_html
```

Or use the helper script:

```bash
bash scripts/coverage_report.sh
```

Tests live under each app's `tests/` directory and cover models, views, forms, API endpoints, scheduler logic, access policies, and Gemini integration.

---

## Docker

Build and run with Docker:

```bash
docker build -t digital-healthcare .
docker run -p 8000:8000 digital-healthcare
```

The container exposes port **8000** and runs Django's development server by default. For production, replace the `CMD` with a WSGI server such as Gunicorn and configure a production database.

---

## CI / Coverage

GitHub Actions runs on every push and pull request to `main`:

1. Installs Python 3.11 and project dependencies
2. Runs pytest with coverage (`--cov-fail-under=90`)
3. Uploads an HTML coverage artifact

Workflow file: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

Coverage configuration: [`.coveragerc`](.coveragerc) (migrations and test files omitted from reports).

---

## Scheduling API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/Appointments/api/doctors/<doctor_id>/availability/` | List available time slots |
| `POST` | `/Appointments/api/appointments/` | Book an appointment atomically |

### GET availability

**Query parameters:** `start`, `end` (ISO 8601 datetimes), `duration` (minutes, default `30`)

```http
GET /Appointments/api/doctors/1/availability/?start=2024-07-10T09:00:00%2B03:00&end=2024-07-10T17:00:00%2B03:00&duration=30
```

**Response:**

```json
{
  "slots": [
    {"start": "2024-07-10T09:00:00+03:00", "end": "2024-07-10T09:30:00+03:00"}
  ]
}
```

### POST create appointment

Requires an authenticated user authorized by the appointment policy.

```json
{
  "doctor_id": 1,
  "patient_id": 2,
  "slot_start": "2024-07-10T09:00:00+03:00",
  "duration": 30
}
```

**Responses:** `200` (created), `401` (unauthenticated), `403` (forbidden), `409` (slot conflict)

---

## Access Control

The `access` app centralizes authorization:

| Role | Detected via |
|------|--------------|
| `admin` | Django superuser or staff |
| `doctor` | Linked `Doctor` profile |
| `patient` | Linked `Patient` profile |
| `anonymous` | Unauthenticated |

Policy functions in `access/policy.py` govern appointment CRUD. Decorators in `access/decorators.py` enforce authentication and policy checks on views and API endpoints.

---

## URL Overview

### Patients (`/Patients/`)

| Path | Name |
|------|------|
| `PatientSignUp/` | Patient registration |
| `PatientLogin/` | Patient login |
| `PatientDashboard/<pk>` | Dashboard |
| `PatientProfile/` | Profile management |
| `GeminiChat/` | AI health assistant |
| `medical-history/<patient_id>` | View medical history |
| `add-diagnostic-results/<patient_id>` | Add diagnostics (doctor use) |

### Doctors (`/Doctors/`)

| Path | Name |
|------|------|
| `DoctorSignUp/` | Doctor registration |
| `DoctorLogin/` | Doctor login |
| `BrowseDoctors/` | Search and filter doctors |
| `DoctorDetail/<pk>` | Doctor profile page |
| `Posts/` | Doctor blog posts |
| `activate/<uidb64>/<token>/` | Email verification |

### Appointments (`/Appointments/`)

| Path | Name |
|------|------|
| `schedule_appointment/<doctor_id>/` | Book appointment |
| `confirm_appointment/<id>/` | Doctor confirms |
| `reschedule_appointment/<id>/` | Reschedule |
| `edit_appointment/<id>/` | Edit details |
| `delete_appointment/<id>/` | Cancel |
| `VideoCall/<id>/` | Start video call |

---

## Screenshots & Media

User-uploaded files (doctor photos, verification documents) are stored under `media/`. Static assets (CSS, JavaScript) are served from `static/` and app-specific static directories.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-change`)
3. Write tests for new behavior
4. Ensure coverage stays at or above **90%**
5. Open a pull request against `main`

---

## License

This project is provided as-is for educational and development purposes. Add a license file here if you intend to open-source under a specific terms.
