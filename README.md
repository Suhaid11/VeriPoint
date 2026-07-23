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
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

---

# VeriPoint

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Features](#features)
4. [Screenshots](#screenshots)
5. [Technology Stack](#technology-stack)
6. [Project Architecture](#project-architecture)
7. [Installation Guide](#installation-guide)
8. [Folder Structure](#folder-structure)
9. [Database Schema Summary](#database-schema-summary)
10. [Usage](#usage)
11. [Future Improvements](#future-improvements)
12. [Contributing](#contributing)
13. [License](#license)

---

## Introduction

**VeriPoint** is a web-based platform that reimagines how consumers evaluate businesses. Traditional review systems rely on subjective star ratings that are easily manipulated. VeriPoint introduces **evidence-backed reviews** where every claim can be supported by photos, invoices, receipts, and documents.

A proprietary **Credibility Score** (0–100) weighs evidence quality, reviewer reputation, community verification, and business engagement to produce a trust metric that both consumers and businesses can rely on.

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
- 💼 **Business Profiles** — Detailed listings with photos, hours, contact info
- 💬 **Business Response** — Official responses with counter-evidence

### User Experience
- 🔍 **Search & Discovery** — Search by name, category, city
- 📂 **Category Browsing** — Hierarchical business categories
- 🔖 **Bookmarks** — Save businesses and reviews
- 🔔 **Notifications** — Real-time activity notifications
- 🏆 **Leaderboard** — Top reviewers by reputation

### Technical
- 🌗 **Dark/Light Mode** — System-aware theme switching
- 📱 **Responsive Design** — Mobile-first, works on all devices
- ♿ **Accessible** — WCAG 2.1 AA compliant
- 🔒 **Secure** — CSRF, XSS, input validation, file upload safety
- ⚡ **Optimized** — Efficient queries, proper indexing, pagination

---

## Screenshots

> Screenshots will be added after implementation is complete.

| Page | Description |
|---|---|
| Landing Page | Hero section with CTA, feature highlights |
| Dashboard | User overview, recent activity, quick stats |
| Business Profile | Business details with reviews and trust scores |
| Review Creation | Evidence upload form with drag-and-drop |
| Leaderboard | Top reviewers ranked by reputation |
| Admin Dashboard | Platform statistics and moderation tools |

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Django 5.x |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Icons** | Lucide Icons (CDN) |
| **Charts** | Chart.js (CDN) |
| **Fonts** | Inter (Google Fonts) |
| **Data Format** | JSON (fixtures, API responses) |

### What We Don't Use (and Why)
- **No CSS frameworks** — Custom design system for full control
- **No JavaScript frameworks** — Vanilla JS for minimal overhead
- **No external databases** — SQLite3 works locally, zero config
- **No paid APIs** — Fully self-contained
- **No Docker** — Simple `python manage.py runserver`

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
| `core` | Base models, static pages, utilities, template tags |
| `accounts` | User auth, profiles, reputation, settings |
| `businesses` | Business listings, categories, photos |
| `reviews` | Reviews, evidence, trust scoring |
| `community` | Votes, comments, business responses, bookmarks |
| `notifications` | Notification system |
| `moderation` | Admin dashboard, audit logs |

---

## Installation Guide

### Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- Git

### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **⚠️ Check "Add Python to PATH"** during installation
4. Verify:
   ```bash
   python --version
   # Expected: Python 3.10.x or later
   ```

**macOS:**
```bash
brew install python@3.12
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/veripoint.git
cd veripoint
```

### Step 3: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` contains:
```
Django>=5.0,<6.0
Pillow>=10.0       # Image processing for uploads
```

### Step 5: Verify SQLite3

SQLite3 comes bundled with Python. Verify it's available:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
# Expected: 3.35.0 or later
```

No additional installation needed.

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the `db.sqlite3` database with all tables.

### Step 7: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin`
- Email: `admin@veripoint.com`
- Password: (choose a strong password)

### Step 8: Load Seed Data (Optional)

```bash
python manage.py seed_data
```

This populates the database with realistic dummy data including businesses, users, reviews, and evidence.

### Step 9: Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Quick Start Summary

```bash
# One-time setup
git clone https://github.com/yourusername/veripoint.git
cd veripoint
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data     # Optional: load demo data

# Run server
python manage.py runserver
```

---

## Folder Structure

```
VeriPoint/
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── db.sqlite3                    # SQLite database (auto-created)
│
├── veripoint/                    # Project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py                   # WSGI entry point
│   └── asgi.py                   # ASGI entry point
│
├── apps/                         # Django applications
│   ├── core/                     # Shared utilities, static pages
│   ├── accounts/                 # Authentication, profiles
│   ├── businesses/               # Business listings
│   ├── reviews/                  # Reviews, evidence, scoring
│   ├── community/                # Votes, comments, responses
│   ├── notifications/            # Notification system
│   └── moderation/               # Admin tools, audit logs
│
├── templates/                    # Global templates
│   ├── base.html                 # Master template
│   ├── components/               # Reusable UI components
│   └── errors/                   # Error pages (404, 500)
│
├── static/                       # Static assets
│   ├── css/                      # Stylesheets
│   ├── js/                       # JavaScript
│   ├── images/                   # Images and icons
│   └── fonts/                    # Web fonts
│
├── media/                        # User uploads (gitignored)
│
└── fixtures/                     # JSON seed data
```

---

## Database Schema Summary

VeriPoint uses **17 models** across 7 Django apps:

| Model | Records | Purpose |
|---|---|---|
| User | Auth | Extended user with roles |
| UserProfile | 1:1 User | Avatar, bio, preferences |
| Category | Hierarchical | Business categorization |
| Business | Core | Business listings |
| BusinessPhoto | Gallery | Business images |
| Review | Core | Evidence-based reviews |
| Evidence | Core | Review attachments (files) |
| EvidenceVerification | Trust | Community evidence checks |
| TrustScore | Core | 0–100 credibility score |
| Comment | Social | Threaded review comments |
| Vote | Social | Review upvotes/downvotes |
| BusinessResponse | Trust | Official business replies |
| Bookmark | UX | Saved items |
| Notification | UX | Activity notifications |
| Reputation | Trust | Reviewer reputation tiers |
| AuditLog | Admin | Administrative action log |
| ActivityLog | Admin | User activity tracking |

For the complete schema with ER diagram, field definitions, indexes, and optimization strategy, see [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md).

---

## Usage

### For Reviewers
1. **Register** an account
2. **Find** a business via search or category browsing
3. **Write a review** with title, body, and visit date
4. **Attach evidence** — upload photos, invoices, receipts
5. **Submit** — the Credibility Score is calculated automatically
6. **Engage** — respond to comments, earn reputation

### For Business Owners
1. **Register** as a Business Owner
2. **Create** your business listing
3. **Respond** to reviews with official responses
4. **Attach** counter-evidence when appropriate
5. **Monitor** your business analytics

### For Admins
1. Access the **Admin Dashboard** at `/admin-dashboard/`
2. **Moderate** reviews, evidence, and comments
3. **Manage** users and businesses
4. **Review** audit logs for compliance

---

## Future Improvements

- [ ] SMTP email verification
- [ ] Two-factor authentication (2FA)
- [ ] QR-code based review collection
- [ ] REST API (Django REST Framework)
- [ ] Advanced analytics with export
- [ ] Machine learning for fake review detection
- [ ] Progressive Web App (PWA)
- [ ] Multi-language support (i18n)
- [ ] Social login (Google, GitHub)
- [ ] Webhook integrations
- [ ] Business premium plans

---

## Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes:
   ```bash
   git commit -m "Add: your feature description"
   ```
4. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open** a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use Django conventions for models, views, and templates
- Write meaningful commit messages
- Add docstrings to all functions and classes
- Keep templates DRY using inheritance and includes

### Commit Message Format
```
Add: new feature description
Fix: bug description
Update: what was changed
Remove: what was removed
Refactor: what was improved
```

---

## License

This project is licensed under the **MIT License**.

```
MIT License

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
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Built with 🛡️ by the VeriPoint Team
  <br>
  <em>Verify Before You Trust.</em>
</p>
