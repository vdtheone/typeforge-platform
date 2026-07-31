# ⌨️ TypeForge - AI-Powered Typing Platform

A next-generation typing speed test platform inspired by Monkeytype. Built with modern web technologies and enhanced with AI-powered analytics, multiplayer racing, deep customization, and structured learning systems.

---

## ✨ Features

- **Ultra-low Latency Typing Engine:** Custom-built React typing engine optimized for raw performance and exact keystroke accuracy.
- **AI Analytics & Insights:** Identifies weak fingers, tricky bigrams, and suggests tailored practice texts.
- **Multiplayer Racing:** Real-time competitive typing tests against friends or global players.
- **Deep Customization:** Fully themable UI with customizable fonts, caret styles, and sound profiles.
- **Global Leaderboards:** Track your rank across various time and word-count formats.

## 🛠 Tech Stack

**Frontend**
- Next.js 14+ (App Router)
- React & TypeScript
- Tailwind CSS
- Zustand (State Management)

**Backend**
- Python 3 & Django
- Django REST Framework (DRF)
- PostgreSQL & Redis (via Docker)
- Celery (Background Tasks)

## 🏗️ Project Architecture

This is a monorepo containing both the frontend and backend applications:

*   **`backend/`**: The Django API, providing core services, authentication, AI analytics, and leaderboards.
*   **`frontend/`**: The Next.js web application, delivering the high-performance user interface.

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- Docker & Docker Compose (optional, for backend databases/cache)

### Quick Start

You can run both the frontend and backend simultaneously using the provided start script from the root directory:

```bash
./start.sh
```

*(Note: The script will automatically start the backend on port 8001 and the frontend on port 3000)*

### Manual Setup

If you prefer to start services individually or need advanced configuration, please refer to the specific documentation for each component:

*   [Backend Setup Guide](./backend/README.md)
*   [Frontend Setup Guide](./frontend/README.md)

## 🐳 Docker Support

You can easily run the backend services and databases using the provided Docker Compose configuration:

```bash
cd backend/docker
docker-compose up -d
```

## 📄 License

This project is licensed under the MIT License.

---

## 📌 Repository Info

| Field | Details |
|---|---|
| **GitHub** | [vdtheone/typeforge-platform](https://github.com/vdtheone/typeforge-platform) |
| **Local Path** | `/home/neosoft/vishal/Django/typeforge-platform` |
| **Main Branch** | `main` |
| **Tech Stack** | Django, DRF |
| **Migrated** | 2026-07-31 — moved from VishalNeosoft24 → vdtheone |

### 🔄 Git Remote
```bash
git remote set-url origin git@github.com:vdtheone/typeforge-platform.git
```

### 📋 Quick Commands
```bash
# Check status
git status

# Push changes
git push origin main

# Pull latest
git pull origin main
```

