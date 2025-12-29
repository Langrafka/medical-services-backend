# medical-services-backend

This repository contains the Backend API (Python) part of our web service for booking home medical services.

### Description

Initial API setup including Docker configuration (Nginx, Postgres, Gunicorn) and core database models (CRM, Operations,
Web Content).

### How to test

1. **Environment Setup:**
   Create `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env

Build and Run Containers:

Bash

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
Database & Static Files Setup: Note: Migrations are already included in the repo.

Bash

docker compose exec api python manage.py migrate
docker compose exec api python manage.py collectstatic --no-input
Create Admin User:

Bash

docker compose exec api python manage.py createsuperuser
Verify: Go to: http://localhost/admin (or https:// if SSL is configured) Log in with the credentials created in step 4.

Endpoints:

- Contact form endpoint: http://localhost:8000/api/contact_form
- Career form endpoint: http://localhost:8000/api/career_form
- Services endpoint: http://localhost:8000/api/services
- Swagger-UI endpoint: http://localhost:8000/api/schema/swagger-ui
