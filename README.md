# ADvantage Platform – Local Setup Guide

Welcome to the official repository for the [ADvantage Platform](https://github.com/ADvantage4/ADvantage) — a personalized AI-based ad generation and campaign manager.

This guide will help you run the ADvantage platform **locally** on your machine.

---

## Prerequisites

- Python 3.9+
- PostgreSQL installed and running
- Git
- VS Code or any code editor

---

## Step-by-Step Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ADvantage4/ADvantage.git
cd ADvantage
```

---

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Navigate to the AD_gen Module and Install Its Requirements

> Replace the path if you're not in the root.

```bash
cd ./AD_gen/
pip install -r requirements.txt
cd ..
```

---

## Database Configuration

### Update `settings.py` with the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'advantage_db2',
        'USER': 'postgres',
        'PASSWORD': 'yourpass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Create `.env` Files

### In the **root directory**, create a `.env` file:

```env
EMAIL_HOST_USER=GMAIL_ADDRESS_TO_PUSH
EMAIL_HOST_PASSWORD=PASSWORD
DATABASE_URL=postgresql://advantage_admin:Advantage%40123@localhost:5432/advantage_db
SECRET_KEY=your-django-secret-key
DEBUG=True
OPENAI_API_KEY=your-own-openai-api-key  # Replace this with your personal key

DB_NAME=advantage_db2
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

---

### In the **AD_gen/** folder, create another `.env` file:

```env
# Google Trends & Search Tokens
GOOGLE_CX=YOUR_CX_KEY
GOOGLE_API_KEY=YOUR_API_KEY
# OpenAI API Key
OPENAI_API_KEY=YOUR_API_KEY  # Replace this with your key

# Database Connection
DB_NAME=advantage_db2
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

---

## Run Migrations

### 1. Apply `user_auth` migrations:

```bash
python manage.py makemigrations user_auth
python manage.py migrate user_auth
```

### 2. Manually Create Required Tables via PostgreSQL Terminal

```sql
CREATE TABLE IF NOT EXISTS public.google_trends_now (
  id           SERIAL PRIMARY KEY,
  topic        TEXT     NOT NULL,
  volume       BIGINT,
  start_time   TIMESTAMP WITH TIME ZONE,
  scraped_date DATE     NOT NULL,
  summary      TEXT,
  inserted_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.google_trends_7d (
  id           SERIAL PRIMARY KEY,
  topic        TEXT     NOT NULL,
  volume       BIGINT,
  start_time   TIMESTAMP WITH TIME ZONE,
  scraped_date DATE     NOT NULL,
  summary      TEXT,
  inserted_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 3. Apply the remaining migrations:

```bash
python manage.py makemigrations manage_cust
python manage.py migrate manage_cust
python manage.py migrate
```

---

## ▶️Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/auth/admin-login/
```

---

## Admin Login

- **Username**: `superuser`
- **Password**: `admin`

Click **"Add new Data & News"** to fetch and store the latest trends into the database.

---

## Try the Platform

1. Sign up: [http://127.0.0.1:8000/auth/signup/](http://127.0.0.1:8000/auth/signup/)
2. Login: [http://127.0.0.1:8000/auth/login/](http://127.0.0.1:8000/auth/login/)
3. Fill out the ad generation form and start creating campaigns!

---

## Need Help?

Raise an issue in this repository or email us at **advantage.bluemelon@gmail.com**.

---
