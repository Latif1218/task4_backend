# Service Marketplace - Backend (FastAPI + PostgreSQL)

## Tech Stack
- FastAPI
- PostgreSQL (SQLAlchemy ORM)
- JWT Authentication (python-jose)
- Alembic (Database Migration)

## Local Setup (Using PostgreSQL)

### 1. Create a PostgreSQL Database
```bash
psql -U postgres
CREATE DATABASE marketplace_db;
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the .env File
```bash
cp .env.example .env
```
Then set `DATABASE_URL` and `SECRET_KEY` correctly in the `.env` file.

### 5. Run Migrations with Alembic
```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### 6. Insert Seed Data (Sample Admin/Vendor/User/Service)
```bash
python -m scripts.seed_data
```

### 7. Start the Server
```bash
uvicorn app.main:app --reload
```

API will run at: `http://localhost:8000`
Swagger Docs: `http://localhost:8000/docs`

## Test Login (Using Seed Data)
| Role   | Email                  | Password   |
|--------|------------------------|------------|
| Admin  | admin@marketplace.com  | Admin123!  |
| Vendor | vendor@marketplace.com | Vendor123! |
| User   | user@marketplace.com   | User123!   |

## Running with Docker (For VPS Deployment)
```bash
docker-compose up --build -d
```

## Mock Payment Testing
During Checkout, if the Card Number ends in `0000`, the Payment will simulate a Failure.
Any other number will result in a Successful Payment.
