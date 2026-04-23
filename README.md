# Kittygram

A full-stack web application for sharing photos of your cats and tracking their achievements.  
React SPA frontend + Django REST Framework backend, fully containerised with Docker Compose and a CI/CD pipeline via GitHub Actions.

---

## Features

- **Registration & authentication** — Djoser-based token auth
- **Cat cards** — create, edit, and delete entries with name, colour (hex → CSS name), birth year, and photo upload (Base64)
- **Achievements** — attach custom achievement tags to any cat
- **Age calculation** — computed automatically from birth year on every API response
- **Paginated API** — `PageNumberPagination` on cat list endpoint
- **React SPA** — client-side routing, protected routes, modal confirmations
- **CI/CD** — push to `main` triggers lint → test → Docker Hub build → SSH deploy → Telegram notification

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9, Django 3.2, Django REST Framework 3.12 |
| Auth | Djoser 2.1 |
| Database | PostgreSQL 13 |
| Frontend | React 18, CSS Modules |
| Gateway | Nginx |
| Infrastructure | Docker Compose, GitHub Actions |
| Linting | Ruff |
| Testing | pytest, pytest-django, Django test runner, React Testing Library |

---

## Quick Start

```bash
cp .env.example .env   # fill in secrets
docker compose up --build
```

App available at `http://localhost:9000`.

---

## Environment Variables (`.env`)

```env
POSTGRES_DB=kittygram
POSTGRES_USER=kittygram
POSTGRES_PASSWORD=kittygram
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:9000
```

---

## Running Tests Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py test

# Linting
ruff check backend

# Frontend
cd frontend
npm ci
npm test -- --watchAll=false

# Integration (pytest against a live deployment)
# Fill tests.yml with repo_owner, domains, dockerhub_username
pytest
```

---

## CI/CD Pipeline

```
push → main
  │
  ├── tests          ruff lint + Django tests + React tests
  ├── build_and_push build backend / frontend / gateway images → Docker Hub
  ├── deploy         SSH into server, write .env, docker compose pull + up -d
  └── telegram       notify on success
```

Secrets required in GitHub repository settings:

`DOCKER_USERNAME`, `DOCKER_PASSWORD`, `HOST`, `USER`, `SSH_KEY`, `SSH_PASSPHRASE`, `POSTGRES_*`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `TELEGRAM_TO`, `TELEGRAM_TOKEN`

---

## Project Structure

```
kittygram/
├── backend/               # Django project
│   ├── cats/              # models, serializers, viewsets
│   └── kittygram_backend/ # settings, urls
├── frontend/              # React SPA
│   └── src/components/    # page components + UI kit
├── nginx/                 # gateway Dockerfile + nginx.conf
├── docker-compose.yml              # local dev
├── docker-compose.production.yml   # production
└── .github/workflows/main.yml      # CI/CD
```

---

## API Highlights

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/token/login/` | Obtain auth token |
| `GET/POST /api/cats/` | List / create cats |
| `GET/PATCH/DELETE /api/cats/{id}/` | Retrieve / update / delete cat |
| `GET/POST /api/achievements/` | List / create achievements |

Colour field accepts hex values (`#ff0000`) and stores the CSS colour name. Images are accepted as Base64 data URIs.

---

## Author

- GitHub: [Shipovmax](https://github.com/Shipovmax)
- Email: shipov.max@icloud.com
