# Campus Sports Booking Backend

Backend-ul platformei web de rezervare a terenurilor de sport si a bazinului USV.

## Structura

```text
backend/              Python + FastAPI + SQLAlchemy
docs/                 Documentatie si contractul OpenAPI
.github/workflows/    Pipeline-uri CI (GitHub Actions)
docker-compose.yml    PostgreSQL + backend
```

## Pornire cu Docker

```bash
cp .env.example .env
docker compose up --build
```

API-ul porneste pe `http://localhost:8000/api/v1`, iar documentatia Swagger e la
`http://localhost:8000/docs`.

Doar baza de date:

```bash
docker compose up -d db
```

## Pornire locala (fara Docker pentru backend)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # pe Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## De adaugat

- `docs/campus-sports-booking-api.yaml`: contractul exportat din Swagger Editor
- `.github/workflows/`: pipeline-ul CI
