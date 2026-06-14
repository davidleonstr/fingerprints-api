# FINGERPRINT ATTENDANCE SYSTEM - API

A RESTful API built with Flask for managing fingerprint-based attendance tracking. It supports role-based access control via JWT and API key authentication.

---

## Prerequisites

- Python 3.10+
- PostgreSQL
- `pip`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davidleonstr/fingerprints-api.git
cd fingerprints-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install manually:
> ```bash
> pip install flask flask-sqlalchemy psycopg2-binary pydantic python-dotenv pyjwt bcrypt
> ```

---

## Database Setup

### 1. Create the PostgreSQL database

Use this repository.

```sql
git clone https://github.com/davidleonstr/fingerprints-db.git
```

### 2. Make sure your PostgreSQL user has access

The default config expects:
- **User:** `postgres`
- **Password:** `root`
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `fingerprints`

---

## Environment Configuration

Create a `.env` file at the root of the project:

```env
API_HOST='localhost'
API_PORT=9000
API_KEY='your-api-key-here'
SQLALCHEMY_DATABASE_URI='postgresql://postgres:root@localhost:5432/fingerprints'
SQLALCHEMY_TRACK_MODIFICATIONS=False
JWT_SECRET='your-jwt-secret-here'
PASSWORD_SALT='your-bcrypt-salt-here'
```

To generate a bcrypt salt for `PASSWORD_SALT`, run:

```python
import bcrypt
print(bcrypt.gensalt().decode('utf-8'))
```

---

## Running the API

```bash
python main.py
```

The server will start at `http://localhost:9000` by default.

---

## First-Time System Setup

On a fresh database, you need to initialize the system by creating the owner interactor.

### 1. Check if the system is blank

```http
GET /v1/system/blank
x-api-key: your-api-key-here
```

Returns `"true"` if no interactors exist yet.

### 2. Create the owner account

```http
POST /v1/system/owner
x-api-key: your-api-key-here
Content-Type: application/json

{
  "username": "owner",
  "password": "your-password"
}
```

This endpoint is only available when the system is blank and automatically assigns the highest-level role.

---

## Authentication

All endpoints (except `/v1/status/`) require an API key header:

```
x-api-key: your-api-key-here
```

Most endpoints also require a Bearer JWT token:

```
Authorization: Bearer <token>
```

To obtain a token:

```http
POST /v1/auth/
x-api-key: your-api-key-here
Content-Type: application/json

{
  "username": "owner",
  "password": "your-password"
}
```

---

## Permission Levels

| Level | Description     |
|-------|-----------------|
| 1     | Read-only       |
| 2     | Moderator       |
| 3     | Admin           |
| 4     | Owner           |

---

## API Overview

| Resource              | Base URL                        |
|-----------------------|---------------------------------|
| Status                | `/v1/status/`                   |
| Auth                  | `/v1/auth/`                     |
| System                | `/v1/system/`                   |
| Entities              | `/v1/entity/`                   |
| Interactors           | `/v1/interactor/`               |
| Assistable            | `/v1/assistable/`                  |
| Roles                 | `/v1/role/`                     |
| Permission Levels     | `/v1/permission-level/`         |
| Attendance            | `/v1/attendance/`               |
| Attendance Day Times  | `/v1/attendance-day-time/`      |
| Attendance Methods    | `/v1/attendance-method/`        |
| Fingerprints          | `/v1/fingerprint/`              |
| Fingerprint Names     | `/v1/fingerprint-name/`         |
| Fingerprint Types     | `/v1/fingerprint-type/`         |

All resources support standard CRUD operations (`GET`, `POST`, `PUT`, `DELETE`) where applicable.
