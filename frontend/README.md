# ⌨️ AI-Powered Typing Platform — Frontend Development Instructions

This document defines the frontend architecture, UI/UX standards, coding practices, project structure, performance expectations, animation system, and implementation guidelines for building the AI-powered typing platform frontend.

The goal is to build a production-grade, ultra-fast, visually premium typing experience with scalable architecture and enterprise-level frontend engineering practices.

---

# 🎯 Frontend Objectives

The frontend must provide:

* Ultra-low latency typing experience
* Premium modern UI/UX
* Smooth animations and transitions
* Real-time multiplayer synchronization
* Fully responsive layouts
* Accessibility-compliant interfaces
* High scalability and maintainability
* PWA-ready architecture
* Production-level performance optimization

---

# 🏗️ Required Frontend Stack

## Core Framework

| Technology           | Required Usage            |
| -------------------- | ------------------------- |
| Next.js (App Router) | Main frontend framework   |
| React                | Component architecture    |
| TypeScript           | Mandatory for type safety |
| Tailwind CSS         | Styling system            |
| Framer Motion        | Animation system          |
| Zustand              | Global state management   |
| TanStack Query       | Server state management   |
| Socket.io Client     | Real-time communication   |
| shadcn/ui            | Base UI component system  |

---

# 📂 Required Project Structure

```bash
frontend/
│
├── public/
│
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   ├── dashboard/
│   │   ├── race/
│   │   ├── settings/
│   │   ├── analytics/
│   │   └── typing/
│   │
│   ├── components/
│   │   ├── common/
│   │   ├── typing/
│   │   ├── charts/
│   │   ├── multiplayer/
│   │   ├── animations/
│   │   ├── layout/
│   │   └── ui/
│   │
│   ├── hooks/
│   ├── stores/
│   ├── services/
│   ├── providers/
│   ├── types/
│   ├── styles/
│   ├── lib/
│   └── utils/
│
├── tests/
└── README.md
```

---

# ⚡ Typing Engine Requirements

The typing engine is the highest-priority frontend module and must be optimized aggressively.

---

# Typing Engine Rules

## DO NOT

* Do not use controlled `<input>` components
* Do not trigger React re-renders on every keystroke
* Do not use expensive DOM updates
* Do not store every character in global state

---

## MUST USE

* Raw `keydown` event listeners
* Refs for mutable typing state
* requestAnimationFrame for caret updates
* Incremental rendering updates
* Debounced calculations
* Memoized components

---

# Character Data Model

```ts
type CharacterState = {
  char: string;
  typed: string | null;
  state: 'correct' | 'incorrect' | 'extra' | 'pending';
};
```

---

# 🎨 UI/UX Design Standards

The platform UI must feel modern, premium, smooth, and highly polished.

---

# Design Language

## Required Design Principles

* Minimalistic interface
* Clean typography
* Modern spacing system
* Soft shadows
* Smooth transitions
* Glassmorphism where appropriate
* Dark-first design approach
* Responsive layouts
* Accessibility-friendly colors

---

# Typography Rules

* Use fluid typography scaling
* Maintain proper text hierarchy
* Ensure readability across devices
* Use modern font pairings

---

# Color System

All colors must use CSS variables.

Example:

```css
:root {
  --bg-primary: #111111;
  --bg-secondary: #1a1a1a;

  --text-primary: #ffffff;
  --text-secondary: #a1a1aa;

  --accent-primary: #f59e0b;
}
```

---

# 🎞️ Animation Standards

Animations must feel smooth, intentional, and lightweight.

---

# Required Animation Library

Use:

* Framer Motion

---

# Animation Rules

## MUST HAVE

* Route transitions
* Hover effects
* Typing caret animation
* Modal transitions
* Dropdown animations
* Loading skeleton animations
* Multiplayer progress animations

---

## Animation Performance Rules

* Prefer transforms over layout changes
* Use GPU-accelerated animations
* Avoid layout thrashing
* Avoid unnecessary motion
* Respect reduced motion preferences

---

# 📱 Responsive Design Requirements

The platform must be fully responsive.

---

# Required Breakpoints

| Device     | Support   |
| ---------- | --------- |
| Mobile     | Mandatory |
| Tablet     | Mandatory |
| Desktop    | Mandatory |
| Ultra-wide | Supported |

---

# Mobile Requirements

* Touch-friendly controls
* Responsive typography
* Mobile race experience
* Mobile analytics support
* PWA install support

---

# 🌐 Real-Time Multiplayer Requirements

The frontend must support real-time synchronization.

---

# Multiplayer Features

* Live race progress
* Matchmaking lobby
* Countdown system
* Live rankings
* Spectator mode
* Room joining
* Realtime updates

---

# WebSocket Integration Rules

Use:

* Socket.io Client

Architecture:

```text
Frontend
   ↓
Socket.io Client
   ↓
WebSocket Gateway
   ↓
Realtime Updates
```

---

# 📊 Analytics Dashboard Requirements

The analytics dashboard must provide visually rich data representation.

---

# Required Charts

* WPM graph
* Accuracy graph
* Consistency graph
* Typing heatmaps
* Progress timeline
* Weak key analysis

---

# Recommended Libraries

* Recharts
* Chart.js

Optional:

* D3.js for advanced visualizations

---

# 🧠 State Management Rules

## Global State

Use Zustand for:

* User preferences
* Theme settings
* Multiplayer state
* UI state

---

## Server State

Use TanStack Query for:

* API caching
* Retry handling
* Optimistic updates
* Background synchronization

---

# 🔌 API Integration Standards

## API Layer Requirements

Create centralized API service modules.

Example structure:

```bash
services/
├── auth.service.ts
├── typing.service.ts
├── analytics.service.ts
├── multiplayer.service.ts
└── leaderboard.service.ts
```

---

# API Rules

* Centralized error handling
* Automatic token refresh
* Typed API responses
* Retry mechanisms
* Loading state handling

---

# ⚡ Performance Optimization Requirements

Performance is a core product requirement.

---

# Required Optimizations

## Rendering

* React.memo
* useMemo
* useCallback
* Dynamic imports
* Lazy loading
* Component splitting

---

## Animation

* requestAnimationFrame
* GPU transforms
* Motion optimization

---

## Network

* API caching
* Request deduplication
* Lazy-loaded routes

---

# 🔒 Frontend Security Requirements

The frontend must follow modern security standards.

---

# Required Security Features

* Secure JWT handling
* Protected routes
* XSS prevention
* CSRF protection
* Input sanitization
* API validation

---

# 🧪 Testing Requirements

Testing is mandatory.

---

# Required Testing Stack

| Tool                  | Usage             |
| --------------------- | ----------------- |
| Vitest                | Unit Testing      |
| React Testing Library | Component Testing |
| Playwright            | E2E Testing       |

---

# Required Test Coverage

* Typing engine logic
* API hooks
* Multiplayer flows
* Authentication flows
* Critical UI components

---

# 📱 PWA Requirements

The frontend must behave like a native application.

---

# Required PWA Features

* Offline support
* Install prompt
* Background caching
* Push notifications
* Mobile app-like experience

---

# ☁️ Deployment Requirements

## Recommended Platforms

| Platform         | Usage           |
| ---------------- | --------------- |
| Vercel           | Primary Hosting |
| Cloudflare Pages | Edge Deployment |

---

# CI/CD Requirements

Must support:

* Automated builds
* Linting
* Testing pipelines
* Preview deployments

---

# 🌿 Git Branch Strategy

---

# Main Branches

```bash
main
develop
staging
```

---

# Frontend Feature Branches

```bash
feature/typing-ui-system
feature/typing-engine-ui
feature/theme-engine
feature/dashboard-ui
feature/realtime-race-ui
feature/premium-animations
feature/analytics-dashboard
```

---

# 🧪 Development Phases

---

# Phase 1 — Foundation

Implement:

* Project setup
* Design system
* Authentication UI
* Base layout
* Theme engine

---

# Phase 2 — Typing Experience

Implement:

* Typing engine
* Caret system
* Typing animations
* Results screen
* Statistics UI

---

# Phase 3 — Multiplayer

Implement:

* Matchmaking UI
* Realtime races
* Rankings
* Race synchronization

---

# Phase 4 — Analytics & AI

Implement:

* Analytics dashboard
* Heatmaps
* AI trainer UI
* Personalized insights

---

# Phase 5 — Production Polish

Implement:

* Performance optimization
* Accessibility improvements
* SEO optimization
* PWA support
* Animation refinement

---

# 🏆 Final Frontend Goal

Build one of the most polished, responsive, visually premium, and performance-optimized typing interfaces on the internet.

The frontend should deliver:

* Exceptional UI/UX
* Smooth animations
* Real-time responsiveness
* Scalable architecture
* Enterprise-grade maintainability
* Premium visual quality
* High-performance typing experience

---

# 📄 License

MIT License

---

# 👨💻 Developer Notes

Every frontend implementation decision should prioritize:

1. Performance
2. User Experience
3. Scalability
4. Maintainability
5. Accessibility
6. Visual Polish
7. Real-time Responsiveness
