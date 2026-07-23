<p align="center">
  <strong>🛡️ VeriPoint</strong>
  <br>
  <em>Verify Before You Trust.</em>
</p>

<p align="center">
  An Evidence-Based Trust Platform that replaces star ratings with proof-backed credibility scoring.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/SQLite3-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Theme-Light%20Only-f8fafc?style=flat-square&logo=css3&logoColor=4f46e5" alt="Light Theme">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

---

# VeriPoint

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Features](#features)
4. [Design System](#design-system)
5. [Screenshots](#screenshots)
6. [Technology Stack](#technology-stack)
7. [Project Architecture](#project-architecture)
8. [Installation Guide](#installation-guide)
9. [Folder Structure](#folder-structure)
10. [Database Schema Summary](#database-schema-summary)
11. [Usage](#usage)
12. [Future Improvements](#future-improvements)
13. [Contributing](#contributing)
14. [License](#license)

---

## Introduction

**VeriPoint** is a web-based platform that reimagines how consumers evaluate businesses. Traditional review systems rely on subjective star ratings that are easily manipulated. VeriPoint introduces **evidence-backed reviews** where every claim is supported by photos, invoices, receipts, and documents.

A proprietary **Credibility Score** (0–100) weighs evidence quality, reviewer reputation, community verification, and business engagement to produce a trust metric that both consumers and businesses can rely on.

The frontend is built on a custom design system — no CSS frameworks, no JavaScript frameworks. One cohesive light theme, responsive across all screen sizes.

---

## Problem Statement

| Problem | Traditional Platforms | VeriPoint Solution |
|---|---|---|
| Fake reviews | No verification mechanism | Evidence attachments required |
| Emotional ratings | 1–5 stars reflect mood | Credibility Score weighs proof |
| No accountability | Anonymous opinions | Reviewer reputation system |
| Unverifiable claims | "Great food!" — says who? | Attach photo, receipt, visit date |
| Business gaming | Competitors post fake negatives | Community verification + audit trail |

---

## Features

### Core
- 🛡️ **Evidence-Attached Reviews** — Upload photos, invoices, receipts, and documents
- 📊 **Credibility Score** — Algorithmic 0–100 trust score per review
- 👥 **Community Verification** — Users verify evidence authenticity
- 💼 **Business Profiles** — Detailed listings with category, location, and trust metrics
- 💬 **Business Response** — Official responses with counter-evidence

### User Experience
- 🔍 **Search & Discovery** — Search by name, category, or city
- 📂 **Category Browsing** — Six curated industry categories
- 🔖 **Bookmarks** — Save businesses and reviews for later
- 🔔 **Notifications** — Activity feed for votes, comments, and verifications
- 🏆 **Leaderboard** — Top reviewers ranked by reputation score

### Technical
- 📱 **Responsive Design** — Mobile, tablet, laptop, and desktop layouts
- ♿ **Accessible** — Semantic HTML, ARIA labels, WCAG AA contrast
- 🔒 **Secure** — CSRF, XSS protection, input validation, safe file uploads
- ⚡ **Lightweight** — No CSS framework, no JS framework, minimal overhead

---

## Design System

VeriPoint uses a fully custom design system built with CSS custom properties. There is **no dark mode** — a single premium light theme is used throughout.

### CSS Architecture

| File | Purpose |
|---|---|
| `static/css/base.css` | Design tokens, CSS reset, base typography |
| `static/css/layout.css` | Containers, grids, section spacing, hero, sidebar layouts |
| `static/css/components.css` | Navbar, buttons, cards, badges, forms, modals, toasts, footer |
| `static/css/utilities.css` | Spacing, color, typography, display, sizing utilities |

### Design Tokens

```css
/* Spacing — 8pt grid */
--space-1: 0.25rem;   /*  4px */
--space-2: 0.5rem;    /*  8px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */

/* Brand */
--primary:       #4f46e5;   /* Indigo */
--accent:        #059669;   /* Emerald (Trust) */

/* Containers */
--container-max:  1240px;
--container-wide: 1440px;
```

### Component Inventory

| Component | Class |
|---|---|
| Primary Button | `.btn .btn-primary` |
| Secondary Button | `.btn .btn-secondary` |
| Outline Button | `.btn .btn-outline` |
| Accent Button | `.btn .btn-accent` |
| Card | `.card` |
| Interactive Card | `.card .card-interactive` |
| Card Footer | `.card-footer` |
| Badge (7 variants) | `.badge .badge-primary` etc. |
| Trust Score Circle | `.trust-score-circle .score-excellent` etc. |
| Form Control | `.form-control` |
| Auth Layout | `.saas-auth-wrapper` |
| Modal | `.modal-backdrop .modal-dialog` |
| Toast | `.toast-container .toast` |

### Responsive Breakpoints

| Breakpoint | Layout |
|---|---|
| `< 768px` — Mobile | Single column, stacked navigation |
| `768–991px` — Tablet | 2-column grids, stacked sidebar |
| `992–1199px` — Laptop | 3-column grids, sidebar active |
| `1200px+` — Desktop | Full layout, max 1240px |
| `1600px+` — Wide | Expanded to 1440px |

---

## Screenshots

> Screenshots will be added after the final build is complete.

| Page | Description |
|---|---|
| Landing Page | Hero with search, category cards, featured businesses |
| Dashboard | 70/30 layout — reviews + sidebar (profile, links, notifications) |
| Business Profile | Business details, gallery, evidence-backed reviews |
| Review Detail | Credibility breakdown bars, evidence gallery, comments |
| Leaderboard | Podium cards + full rankings table |
| Login | Clean 55/45 split — brand panel + minimal form |
| Register | Grouped fields, role selector cards, password strength meter |
| Admin Dashboard | Platform metrics, audit log feed |

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Django 5.x |
| **Database** | SQLite3 |
| **Frontend** | HTML5, Custom CSS (design system), Vanilla JavaScript |
| **Icons** | Lucide Icons (CDN) |
| **Fonts** | Inter + JetBrains Mono (Google Fonts) |
| **Data Format** | JSON (fixtures, API responses) |

### What We Don't Use (and Why)

| Not Used | Reason |
|---|---|
| CSS frameworks (Tailwind, Bootstrap) | Custom design system gives full control |
| JavaScript frameworks (React, Vue) | Vanilla JS — minimal overhead, no build step |
| Dark mode | Single premium light theme, simpler maintenance |
| External databases | SQLite3 — zero config, works locally |
| Docker | Simple `python manage.py runserver` |
| Paid APIs | Fully self-contained |

---

## Project Architecture

```
Browser (HTML/CSS/JS)
        │
        ▼
  Django URL Router
        │
        ▼
  Views (CBV/FBV)  ←→  Forms (Validation)
        │
        ▼
  Django ORM  ←→  Services (scoring.py, services.py)
        │
        ▼
  SQLite3 Database + File System (media/)
```

### Django Apps

| App | Responsibility |
|---|---|
| `core` | Base models, static pages, template tags, context processors |
| `accounts` | User auth, profiles, reputation, settings |
| `businesses` | Business listings, categories |
| `reviews` | Reviews, evidence attachments, trust scoring |
| `community` | Votes, comments, business responses, bookmarks |
| `notifications` | Activity notification system |
| `moderation` | Admin dashboard, audit logs, user directory |

---

## Installation Guide

### Prerequisites

- Python 3.10 or later
- pip
- Git

### Step 1: Install Python

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer — check **"Add Python to PATH"**
3. Verify: `python --version`

**macOS:**
```bash
brew install python@3.12
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/veripoint.git
cd veripoint
```

### Step 3: Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` contains:
```
Django>=5.0,<6.0
Pillow>=10.0
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Load Seed Data (Recommended)

```bash
python manage.py seed_data
```

Populates the database with demo businesses, users, reviews, and evidence so you can explore the platform immediately.

### Step 8: Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Quick Start (Copy-Paste)

```bash
git clone https://github.com/yourusername/veripoint.git
cd veripoint

# Windows
python -m venv venv && venv\Scripts\activate

# macOS/Linux
python3 -m venv venv && source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

### Demo Credentials (after seed_data)

| Role | Username | Password |
|---|---|---|
| Reviewer | `ananya_sharma` | `password123` |
| Business Owner | `dr_sangita_apollo` | `password123` |
| Admin | `admin` | `admin123` |

---

## Folder Structure

```
VeriPoint/
├── manage.py
├── requirements.txt
├── db.sqlite3                        # Auto-created on migrate
│
├── veripoint/                        # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                             # Django applications
│   ├── core/                         # Utilities, static pages, tags
│   ├── accounts/                     # Auth, profiles, reputation
│   ├── businesses/                   # Listings, categories
│   ├── reviews/                      # Reviews, evidence, scoring
│   ├── community/                    # Votes, comments, bookmarks
│   ├── notifications/                # Notification system
│   └── moderation/                   # Admin tools, audit logs
│
├── templates/                        # All HTML templates
│   ├── base.html                     # Master layout
│   ├── navbar.html                   # Sticky navigation
│   ├── footer.html                   # Full + minimal footers
│   ├── accounts/                     # Login, register, dashboard, profile
│   ├── businesses/                   # Listings, detail, categories, form
│   ├── reviews/                      # Review form, detail, leaderboard
│   ├── community/                    # Bookmarks
│   ├── notifications/                # Notification feed
│   ├── moderation/                   # Admin dashboard, audit log
│   ├── components/                   # Reusable partials
│   │   ├── evidence_badge.html
│   │   ├── empty_state.html
│   │   └── pagination.html
│   └── errors/                       # 404, 500
│
├── static/                           # Static assets
│   ├── css/
│   │   ├── base.css                  # Design tokens + reset
│   │   ├── layout.css                # Containers, grids, hero
│   │   ├── components.css            # UI components
│   │   └── utilities.css             # Utility classes
│   ├── js/
│   │   ├── app.js                    # Core JS (icons, toasts, AJAX)
│   │   └── components/
│   │       ├── evidence-viewer.js    # Evidence lightbox
│   │       └── file-upload.js        # Multi-file upload previews
│   └── images/                       # Static images
│
└── media/                            # User uploads (gitignored)
```

---

## Database Schema Summary

VeriPoint uses **17 models** across 7 Django apps:

| Model | Purpose |
|---|---|
| `User` | Extended user with roles (reviewer, owner, admin) |
| `UserProfile` | Avatar, bio, location, website, preferences |
| `Category` | Business category with icon and description |
| `Business` | Business listing — name, address, category, owner |
| `Review` | Evidence-backed review with title, body, visit date |
| `Evidence` | File attachment (photo, invoice, receipt, PDF) |
| `EvidenceVerification` | Community authenticity assessment |
| `TrustScore` | Algorithmic 0–100 credibility score breakdown |
| `Comment` | Threaded comments on reviews |
| `Vote` | Upvote / downvote on reviews |
| `BusinessResponse` | Official owner reply to a review |
| `Bookmark` | Saved business or review |
| `Notification` | Activity notification record |
| `Reputation` | Reviewer reputation points and tier |
| `AuditLog` | Immutable admin action trail |

### Credibility Score Weights

```
Evidence Attachments   40 pts  (8 pts per item, max 5 items)
Reviewer Reputation    20 pts
Community Audit        20 pts  (2 pts per upvote)
Recency Decay          10 pts  (decays over 365 days)
Business Engagement    10 pts  (owner response + comments)
─────────────────────────────
Total                 100 pts
```

---

## Usage

### For Reviewers
1. Register an account (role: Reviewer)
2. Find a business via search or category browsing
3. Click **Write Evidence Review**
4. Fill in title, body, and visit date
5. Upload supporting evidence — photos, invoices, receipts
6. Submit — Credibility Score is calculated automatically
7. Engage with comments and earn reputation

### For Business Owners
1. Register as **Business Owner**
2. Create your business listing
3. Post official responses to reviews
4. Attach counter-evidence where appropriate
5. Monitor trust score trends

### For Platform Admins
1. Access `/admin-dashboard/` for platform metrics
2. Review audit logs at `/moderation/audit-log/`
3. Manage users at `/moderation/users/`
4. Use Django admin at `/admin/` for full model access

---

## Future Improvements

- [ ] SMTP email verification on registration
- [ ] Two-factor authentication (2FA)
- [ ] REST API (Django REST Framework) for mobile clients
- [ ] QR-code based review collection at point of sale
- [ ] Advanced analytics dashboard with CSV export
- [ ] Machine learning for fake review detection
- [ ] Progressive Web App (PWA) support
- [ ] Multi-language support (i18n) — Hindi, Tamil, Telugu
- [ ] Business premium plans and verified badges
- [ ] Webhook integrations for business tools

---

## Contributing

Contributions are welcome. Here's the workflow:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Commit: `git commit -m "Add: description"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

### Coding Standards
- PEP 8 for Python
- Django conventions for models, views, and templates
- Keep templates DRY — use inheritance and `{% include %}`
- Add docstrings to all functions and classes
- No inline styles in templates — use CSS classes from the design system
- No new CSS frameworks — extend the existing utility system

### Commit Format
```
Add: new feature
Fix: bug description
Update: what changed
Remove: what was removed
Refactor: what was improved
Style: CSS / UI changes
```

---

## License

MIT License — see below.

```
Copyright (c) 2026 VeriPoint

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  Built with 🛡️ by the VeriPoint Team &nbsp;·&nbsp; <em>Verify Before You Trust.</em>
</p>
