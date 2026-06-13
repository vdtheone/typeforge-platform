# ⌨️ AI-Powered Typing Platform

A next-generation typing speed test platform inspired by Monkeytype, built with modern web technologies and enhanced with AI-powered analytics, multiplayer racing, deep customization, and structured learning systems.

## 🏗️ Project Architecture

This is a monorepo containing both the frontend and backend applications:

*   **`backend/`**: The Django REST Framework backend API, providing core services, authentication, AI analytics aggregation, and real-time leaderboards.
*   **`frontend/`**: The Next.js frontend application, delivering an ultra-low latency typing experience, multiplayer interactions, and a highly customizable UI.

## 🚀 Getting Started

### Quick Start
You can run both the frontend and backend simultaneously using the provided start script:

```bash
./start.sh
```

### Manual Setup
To get started manually, please refer to the specific documentation for each component:

*   [Backend Setup Guide](./backend/README.md)
*   [Frontend Setup Guide](./frontend/README.md)

## 🐳 Docker Support

You can run the backend services using the provided Docker Compose configuration inside the `backend/docker/` directory.

## 📄 License

MIT License
