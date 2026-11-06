# Campus Sports Booking

Platforma web de rezervare a terenurilor de sport si a bazinului USV.

## Structura

```text
frontend/             React 19 + TypeScript + Vite (SPA + PWA)
backend/              Python + FastAPI + SQLAlchemy + Alembic
docs/                 Documentatie si contractul OpenAPI
.github/workflows/    Pipeline-uri CI (GitHub Actions)
docker-compose.yml    Serviciile locale (deocamdata doar PostgreSQL)
```

## Stadiu

Acesta este doar scheletul proiectului: folderele sunt pregatite, dar aplicatiile
nu sunt inca initializate.

De adaugat:

- `docs/campus-sports-booking-api.yaml`: contractul exportat din Swagger Editor
- `frontend/`: proiectul Vite, `Dockerfile`, `nginx.conf`
- `backend/`: `app/main.py`, `requirements.txt`, `Dockerfile`, migrarile Alembic
- `.github/workflows/`: pipeline-ul CI
- serviciile `frontend` si `backend` in `docker-compose.yml`

## Pornirea bazei de date

```bash
cp .env.example .env
docker compose up -d db
```
