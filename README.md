<<<<<<< HEAD
# Service Marketplace - Backend (FastAPI + PostgreSQL)

## Tech Stack
- FastAPI
- PostgreSQL (SQLAlchemy ORM)
- JWT Authentication (python-jose)
- Alembic (Database Migration)

## Local Setup (PostgreSQL দিয়ে)

### ১. PostgreSQL Database তৈরি করুন
```bash
psql -U postgres
CREATE DATABASE marketplace_db;
```

### ২. Virtual Environment তৈরি ও Activate করুন
```bash
python -m venv venv
source venv/bin/activate      # Windows-এ: venv\Scripts\activate
```

### ৩. Dependencies Install করুন
```bash
pip install -r requirements.txt
```

### ৪. .env ফাইল তৈরি করুন
```bash
cp .env.example .env
```
তারপর `.env` ফাইলে `DATABASE_URL` ও `SECRET_KEY` ঠিকভাবে সেট করুন।

### ৫. Alembic দিয়ে Migration Run করুন
```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### ৬. Seed Data ঢোকান (Sample Admin/Vendor/User/Service)
```bash
python -m scripts.seed_data
```

### ৭. Server চালু করুন
```bash
uvicorn app.main:app --reload
```

API চলবে: `http://localhost:8000`
Swagger Docs: `http://localhost:8000/docs`

## Seed Data দিয়ে Test Login

| Role   | Email                  | Password   |
|--------|------------------------|------------|
| Admin  | admin@marketplace.com  | Admin123!  |
| Vendor | vendor@marketplace.com | Vendor123! |
| User   | user@marketplace.com   | User123!   |

## Docker দিয়ে চালানো (VPS-এ Deploy করার জন্য)
```bash
docker-compose up --build -d
```

## Mock Payment Testing
Checkout করার সময় Card Number-এর শেষে `0000` দিলে Payment Fail Simulate হবে।
অন্য কোনো Number দিলে Payment Success হবে।
=======
# task4_backend
>>>>>>> 2fd172a714332a0a98b29cad912946e39ebca32c
