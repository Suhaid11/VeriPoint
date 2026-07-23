# VeriPoint — Project Roadmap

> **Verify Before You Trust.**

---

## 1. Project Overview

VeriPoint is an **Evidence-Based Trust Platform** that replaces traditional star-rating review systems with **proof-backed credibility scoring**. Instead of asking *"How many stars?"*, VeriPoint asks *"Where is the proof?"*

Every review on VeriPoint encourages transparency by attaching verifiable evidence — photos, purchase invoices, visit timestamps, and supporting documents. A proprietary **Credibility Score** algorithm weighs the quality and quantity of evidence to produce a trust metric that businesses and consumers can rely on.

---

## 2. Problem Statement

Traditional review platforms suffer from:

| Problem | Impact |
|---|---|
| **Fake reviews** | Businesses buy or fabricate positive reviews |
| **Emotional bias** | Star ratings reflect mood, not facts |
| **No accountability** | Reviewers face no consequence for dishonest reviews |
| **No evidence** | Claims cannot be verified by other users |
| **Gaming** | Competitors post negative reviews to sabotage |
| **Recency bias** | Outdated reviews misrepresent current quality |

There is no mainstream platform that treats **evidence as a first-class citizen** in the review process.

---

## 3. Proposed Solution

VeriPoint introduces:

- **Evidence-Attached Reviews** — Every review can include photos, invoices, bills, timestamps, and documents.
- **Credibility Score** — An algorithmic score (0–100) that weighs evidence quality, reviewer history, community verification, and business response.
- **Community Verification** — Other users can upvote/downvote and verify the authenticity of evidence.
- **Business Response** — Businesses can officially respond to reviews, attach their own evidence, and resolve disputes.
- **Reviewer Reputation** — Users build a reputation score over time based on the quality and consistency of their reviews.
- **Audit Trail** — All actions are logged for transparency and moderation.

---

## 4. Objectives

1. Build a production-quality Django web application with clean architecture.
2. Implement an evidence-first review system with file uploads and verification.
3. Design an efficient, normalized SQLite3 database with proper indexing.
4. Create a premium, responsive SaaS UI with dark/light mode.
5. Follow Django security best practices (CSRF, XSS, input validation).
6. Optimize all database queries to avoid N+1 problems.
7. Populate with realistic dummy data that makes the platform feel live.
8. Ensure accessibility (WCAG 2.1 AA compliance).

---

## 5. User Roles

| Role | Description | Permissions |
|---|---|---|
| **Visitor** | Unauthenticated user | Browse businesses, read reviews, search, view leaderboard |
| **Reviewer** | Registered user | Write reviews, attach evidence, vote, comment, bookmark |
| **Business Owner** | Verified business user | Claim business, respond to reviews, attach counter-evidence, view analytics |
| **Moderator** | Trusted community member | Flag/hide inappropriate content, verify evidence, manage reports |
| **Admin** | Platform administrator | Full CRUD on all models, manage users, view audit logs, site settings |

---

## 6. Core Features

### 6.1 Authentication & User Management
- Registration with email verification (simulated via console backend)
- Login / Logout
- Forgot Password / Reset Password
- Profile management (avatar, bio, social links)
- Account settings (theme preference, notification preferences)

### 6.2 Business Listings
- Business creation with category assignment
- Business profile page (description, photos, hours, location, contact)
- Business search with filters (category, location, rating range)
- Business owner claiming and verification
- Business analytics dashboard (for owners)

### 6.3 Evidence-Based Reviews
- Review creation with structured fields:
  - Title, body text, visit date
  - Evidence attachments (photos, invoices, documents)
  - Evidence type tagging (photo, invoice, receipt, document, screenshot)
- Evidence viewer with lightbox
- Review editing (within 48-hour window)
- Review deletion (soft delete)

### 6.4 Credibility Score Engine
- **Evidence Weight** (0–40 pts): Based on number and type of evidence attached
- **Reviewer Reputation** (0–20 pts): Based on historical review quality
- **Community Verification** (0–20 pts): Based on upvotes vs downvotes
- **Recency** (0–10 pts): More recent reviews score higher
- **Business Response** (0–10 pts): Reviews with business engagement score higher
- Score is recalculated on relevant events (new vote, new evidence, business response)

### 6.5 Community Interaction
- Upvote / Downvote reviews
- Comment on reviews
- Flag inappropriate content
- Verify evidence (community verification)

### 6.6 Business Response System
- Official business responses to reviews
- Counter-evidence attachment
- Dispute resolution status tracking

### 6.7 Notifications
- New review on owned business
- Reply to your review
- Vote on your review
- Business response to your review
- Evidence verified
- System announcements

### 6.8 Discovery & Navigation
- Category browsing with icons
- Full-text search (businesses, reviews)
- Trending businesses
- Recently reviewed
- Top-rated by credibility score

### 6.9 Leaderboard
- Top reviewers by reputation score
- Most verified reviewers
- Most active contributors

### 6.10 Bookmarks
- Save businesses and reviews for later
- Organized bookmark collections

### 6.11 Admin Dashboard
- User management
- Business moderation
- Review moderation
- Evidence moderation
- Audit log viewer
- Platform statistics

---

## 7. Future Scope

- Email verification via SMTP
- Two-factor authentication
- QR-code based review collection for businesses
- API layer (Django REST Framework)
- Advanced analytics and reporting
- Machine learning for fake review detection
- Mobile-responsive PWA
- Multi-language support (i18n)
- Webhook integrations

---

## 8. Folder Structure

```
VeriPoint/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── PROJECT_ROADMAP.md
├── DATABASE_SCHEMA.md
├── README.md
│
├── veripoint/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── accounts/                 # User auth, profiles, settings
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── signals.py
│   │   ├── admin.py
│   │   ├── managers.py
│   │   ├── context_processors.py
│   │   └── templates/accounts/
│   │
│   ├── businesses/               # Business listings, profiles
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/businesses/
│   │
│   ├── reviews/                  # Reviews, evidence, credibility
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── scoring.py            # Credibility score engine
│   │   └── templates/reviews/
│   │
│   ├── community/                # Votes, comments, verification
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/community/
│   │
│   ├── notifications/            # Notification system
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py           # Notification creation helpers
│   │   ├── admin.py
│   │   └── templates/notifications/
│   │
│   ├── moderation/               # Admin dashboard, audit logs
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/moderation/
│   │
│   └── core/                     # Shared utilities, landing, static pages
│       ├── models.py             # Abstract base models
│       ├── views.py              # Landing, about, contact, etc.
│       ├── urls.py
│       ├── mixins.py             # Reusable view mixins
│       ├── utils.py              # Helper functions
│       ├── templatetags/
│       │   └── veripoint_tags.py # Custom template tags/filters
│       ├── management/
│       │   └── commands/
│       │       └── seed_data.py  # Dummy data generation
│       └── templates/core/
│
├── templates/                    # Global templates
│   ├── base.html                 # Master template
│   ├── navbar.html
│   ├── footer.html
│   ├── components/               # Reusable UI components
│   │   ├── card.html
│   │   ├── modal.html
│   │   ├── pagination.html
│   │   ├── search_bar.html
│   │   ├── evidence_badge.html
│   │   ├── toast.html
│   │   └── empty_state.html
│   ├── errors/
│   │   ├── 404.html
│   │   └── 500.html
│   └── emails/                   # Email templates (console backend)
│       ├── verification.html
│       └── password_reset.html
│
├── static/
│   ├── css/
│   │   ├── base.css              # Design system tokens, reset
│   │   ├── components.css        # Reusable component styles
│   │   ├── layout.css            # Grid, flex utilities
│   │   ├── pages/                # Page-specific styles
│   │   │   ├── landing.css
│   │   │   ├── dashboard.css
│   │   │   ├── auth.css
│   │   │   └── ...
│   │   ├── themes/
│   │   │   ├── light.css
│   │   │   └── dark.css
│   │   └── utilities.css         # Spacing, typography helpers
│   │
│   ├── js/
│   │   ├── app.js                # Theme toggle, global handlers
│   │   ├── components/
│   │   │   ├── modal.js
│   │   │   ├── toast.js
│   │   │   ├── search.js
│   │   │   ├── evidence-viewer.js
│   │   │   ├── charts.js
│   │   │   └── file-upload.js
│   │   └── pages/
│   │       ├── dashboard.js
│   │       ├── review-form.js
│   │       └── ...
│   │
│   ├── images/
│   │   ├── logo.svg
│   │   ├── icons/
│   │   ├── hero/
│   │   └── placeholders/
│   │
│   └── fonts/                    # Self-hosted web fonts (Inter)
│
├── media/                        # User uploads (gitignored)
│   ├── avatars/
│   ├── evidence/
│   ├── business_photos/
│   └── documents/
│
└── fixtures/                     # JSON fixtures for seed data
    ├── categories.json
    ├── users.json
    ├── businesses.json
    ├── reviews.json
    └── evidence.json
```

---

## 9. Development Milestones

| # | Milestone | Description | Est. Files |
|---|---|---|---|
| **M0** | Planning & Documentation | Roadmap, schema, README | 3 |
| **M1** | Project Scaffolding | Django project, apps, settings, base template, design system | ~25 |
| **M2** | Authentication System | Registration, login, logout, password reset, profile | ~15 |
| **M3** | Business Listings | Categories, business CRUD, search, business profiles | ~15 |
| **M4** | Review & Evidence Engine | Review creation, evidence upload, credibility scoring | ~20 |
| **M5** | Community Features | Voting, comments, community verification, business response | ~15 |
| **M6** | Notifications & Bookmarks | Notification system, bookmark management | ~10 |
| **M7** | Leaderboard & Discovery | Leaderboard, trending, category browsing | ~10 |
| **M8** | Admin & Moderation | Admin dashboard, audit logs, content moderation | ~10 |
| **M9** | Dummy Data & Polish | Seed command, fixtures, animations, final QA | ~10 |

---

## 10. UI Flow

```
┌─────────────┐
│  Landing     │──→ About / Features / Contact / Help
│  Page        │
└─────┬───────┘
      │
      ▼
┌─────────────┐     ┌──────────────┐
│  Login /     │────→│  Dashboard   │
│  Register    │     │  (Home)      │
└─────────────┘     └──────┬───────┘
                           │
              ┌────────────┼────────────┬──────────────┐
              ▼            ▼            ▼              ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐  ┌──────────┐
        │ Search / │ │ Business │ │ Create   │  │ Profile  │
        │ Browse   │ │ Profile  │ │ Review   │  │ Settings │
        └────┬─────┘ └────┬─────┘ └────┬─────┘  └──────────┘
             │            │            │
             ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Category │ │ Review   │ │ Evidence │
        │ Listing  │ │ Details  │ │ Viewer   │
        └──────────┘ └──────────┘ └──────────┘
```

---

## 11. Navigation Flow

### Public Navigation (Visitor)
```
Logo → Landing
About | Features | Contact | Help
Login | Register
Search Bar (always visible)
Category Browser
```

### Authenticated Navigation (Reviewer)
```
Logo → Dashboard
Search | Browse | Bookmarks | Notifications (bell icon with count)
Profile Dropdown → Profile | Settings | My Reviews | Logout
```

### Business Owner Navigation
```
(All Reviewer nav) + My Business | Business Analytics | Respond to Reviews
```

### Admin Navigation
```
(All Reviewer nav) + Admin Dashboard | Moderation | Audit Logs | Users
```

---

## 12. Technical Architecture

```
┌──────────────────────────────────────────────────┐
│                    Browser                        │
│  HTML5 + CSS3 + Vanilla JS + Chart.js + Lucide   │
└────────────────────┬─────────────────────────────┘
                     │ HTTP (GET/POST)
                     ▼
┌──────────────────────────────────────────────────┐
│              Django Application                   │
│                                                   │
│  ┌─────────┐  ┌──────────┐  ┌─────────────────┐ │
│  │  Views   │  │  Forms   │  │  Template Engine │ │
│  │ (CBV/FBV)│  │(Validate)│  │  (Jinja-like)   │ │
│  └────┬─────┘  └────┬─────┘  └────────┬────────┘ │
│       │              │                 │          │
│  ┌────▼──────────────▼─────────────────▼────────┐│
│  │              Django ORM                       ││
│  │  Models → Managers → QuerySets               ││
│  │  select_related() / prefetch_related()        ││
│  └──────────────────┬───────────────────────────┘│
│                     │                             │
│  ┌──────────────────▼───────────────────────────┐│
│  │           Services / Utilities                ││
│  │  scoring.py │ services.py │ utils.py          ││
│  └──────────────────────────────────────────────┘│
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   SQLite3      │
              │   db.sqlite3   │
              └────────────────┘
              ┌────────────────┐
              │   File System  │
              │   /media/      │
              └────────────────┘
```

### Architecture Decisions

| Decision | Rationale |
|---|---|
| **Class-Based Views (primary)** | DRY, built-in mixins, consistent pattern |
| **Function-Based Views (where simpler)** | AJAX endpoints, simple redirects |
| **Service layer (scoring.py, services.py)** | Business logic separated from views |
| **Custom template tags** | Reusable UI logic across templates |
| **Django signals** | Decouple side effects (notifications, score recalculation) |
| **Abstract base models** | `TimestampedModel` for consistent `created_at`/`updated_at` |
| **Django's auth system** | Battle-tested, extensible via `AbstractUser` |
| **Console email backend** | No SMTP dependency for development |

---

## 13. Security Goals

| Goal | Implementation |
|---|---|
| **CSRF Protection** | Django middleware (enabled by default), `{% csrf_token %}` in all forms |
| **XSS Protection** | Django auto-escaping in templates, `Content-Security-Policy` headers |
| **SQL Injection** | Django ORM parameterized queries (no raw SQL) |
| **Authentication** | Django's `auth` system, `LoginRequiredMixin`, `@login_required` |
| **Authorization** | Custom permission checks, `UserPassesTestMixin` |
| **File Upload Validation** | MIME type checking, file size limits, extension whitelist |
| **Password Security** | Django's `PBKDF2` hasher, password validators |
| **Clickjacking** | `X-Frame-Options: DENY` header |
| **Session Security** | `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE` (production) |
| **Input Validation** | Django forms with field-level validators |
| **Rate Limiting** | Custom middleware for sensitive endpoints |
| **Audit Logging** | All admin/moderation actions logged |

---

## 14. Performance Goals

| Goal | Strategy |
|---|---|
| **Query Efficiency** | `select_related()` for FK, `prefetch_related()` for M2M, avoid N+1 |
| **Database Indexing** | Indexes on all foreign keys, search fields, frequently filtered fields |
| **Template Performance** | Template fragment caching with `{% cache %}` |
| **Static Assets** | `{% static %}` tag, `ManifestStaticFilesStorage` for cache busting |
| **Pagination** | All list views paginated (12–20 items per page) |
| **Lazy Loading** | Images loaded lazily with `loading="lazy"` |
| **Minimal JavaScript** | Vanilla JS only, no framework overhead |
| **CSS Efficiency** | CSS custom properties for theming, minimal specificity |
| **Database** | SQLite WAL mode for concurrent reads |

---

## 15. Scalability Considerations

While SQLite3 is the development database, the architecture is designed for future scalability:

- **Database Abstraction**: All queries go through Django ORM — switching to PostgreSQL requires only a settings change.
- **Modular App Structure**: Each Django app is self-contained and can be extracted into a microservice.
- **Service Layer**: Business logic in service modules, not in views — enables API layer addition.
- **Static Files**: Organized for CDN deployment with `collectstatic`.
- **Media Storage**: Abstracted through Django's storage backend — swappable to S3/GCS.
- **Caching**: Template caching strategy in place — can be backed by Redis/Memcached.
- **Stateless Views**: No server-side session state beyond Django's session framework.

---

## 16. Design System Summary

### Color Palette
```
Primary:        hsl(230, 75%, 55%)    — Deep Indigo
Primary Light:  hsl(230, 75%, 65%)
Primary Dark:   hsl(230, 75%, 40%)

Accent:         hsl(160, 70%, 45%)    — Emerald Green (trust/verification)
Warning:        hsl(40, 95%, 55%)     — Amber
Danger:         hsl(0, 75%, 55%)      — Coral Red
Success:        hsl(145, 65%, 45%)    — Green

Neutral 50:     hsl(220, 15%, 97%)
Neutral 100:    hsl(220, 15%, 93%)
Neutral 200:    hsl(220, 13%, 85%)
Neutral 300:    hsl(220, 12%, 72%)
Neutral 400:    hsl(220, 10%, 55%)
Neutral 500:    hsl(220, 10%, 40%)
Neutral 600:    hsl(220, 12%, 28%)
Neutral 700:    hsl(220, 15%, 18%)
Neutral 800:    hsl(220, 18%, 12%)
Neutral 900:    hsl(220, 20%, 8%)
```

### Typography
- **Headings**: Inter (700, 600)
- **Body**: Inter (400, 500)
- **Monospace**: JetBrains Mono (code/data)

### Spacing Scale
`4px → 8px → 12px → 16px → 24px → 32px → 48px → 64px → 96px`

### Border Radius
`4px (sm) → 8px (md) → 12px (lg) → 16px (xl) → 9999px (full)`

---

*This roadmap is a living document. It will be updated as the project evolves.*
