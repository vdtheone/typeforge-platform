# ⌨️ TypeForge Platform

**AI-Powered Typing Speed Test Platform** — A next-generation typing platform inspired by Monkeytype, built with Django REST Framework and enhanced with AI-powered analytics, multiplayer racing, and deep customization.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis 7+

### Local Development Setup

```bash
# Clone the repository
git clone git@github.com:vdtheone/typeforge-platform.git
cd typeforge-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed data
python manage.py shell < scripts/seed_wordlists.py
python manage.py shell < scripts/seed_themes.py

# Start development server
python manage.py runserver
```

### Docker Setup

```bash
cd docker
docker-compose up -d
```

---

## 📡 API Documentation

After starting the server, visit:
- **Swagger UI**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

---

## 🏗️ Project Structure

```
typeforge-platform/
├── config/                 # Django project settings (split by environment)
├── apps/
│   ├── core/              # Shared utilities, base models, middleware
│   ├── accounts/          # Auth, user profiles, preferences
│   ├── typing_tests/      # Test generation & submission
│   ├── results/           # Test results & history
│   ├── wordlists/         # Word list & language management
│   ├── themes/            # Theme management & sharing
│   ├── analytics/         # Performance analytics engine
│   └── leaderboards/      # Redis-backed ranking system
├── docker/                # Docker configuration
├── scripts/               # Seed data scripts
└── requirements/          # Split dependency files
```

---

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| Django 5.2 | Web Framework |
| Django REST Framework | REST API |
| PostgreSQL | Primary Database |
| Redis | Cache, Leaderboards, Celery Broker |
| Celery | Background Task Processing |
| SimpleJWT | Authentication |
| drf-spectacular | API Documentation |

---

## 📄 License

MIT License
