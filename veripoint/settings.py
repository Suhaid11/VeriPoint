"""
VeriPoint — Django Settings
Evidence-Based Trust Platform

Development configuration. For production deployment,
override SECRET_KEY, DEBUG, ALLOWED_HOSTS, and database settings.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECRET_KEY = 'django-insecure-veripoint-dev-key-change-in-production-2026'

DEBUG = True

ALLOWED_HOSTS = ['*']

# ---------------------------------------------------------------------------
# Application Definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # VeriPoint apps
    'apps.core',
    'apps.accounts',
    'apps.businesses',
    'apps.reviews',
    'apps.community',
    'apps.notifications',
    'apps.moderation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'veripoint.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'veripoint.wsgi.application'

# ---------------------------------------------------------------------------
# Database — SQLite3
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'

# ---------------------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static Files
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------------------------------------------------
# Media Files (User Uploads)
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------------------------
# File Upload Settings
# ---------------------------------------------------------------------------
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

# Allowed evidence file extensions
ALLOWED_EVIDENCE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf']
MAX_EVIDENCE_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_EVIDENCE_PER_REVIEW = 10

# Allowed avatar extensions
ALLOWED_AVATAR_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
MAX_AVATAR_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# ---------------------------------------------------------------------------
# Email (Console backend for development)
# ---------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@veripoint.com'

# ---------------------------------------------------------------------------
# Security Headers
# ---------------------------------------------------------------------------
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# ---------------------------------------------------------------------------
# Default Auto Field
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
ITEMS_PER_PAGE = 12
REVIEWS_PER_PAGE = 10
NOTIFICATIONS_PER_PAGE = 20
LEADERBOARD_SIZE = 20

# ---------------------------------------------------------------------------
# Credibility Score Weights
# ---------------------------------------------------------------------------
TRUST_SCORE_WEIGHTS = {
    'evidence_max': 40,
    'evidence_per_item': 8,
    'reputation_max': 20,
    'community_max': 20,
    'community_per_vote': 2,
    'recency_max': 10,
    'recency_decay_days': 365,
    'engagement_max': 10,
    'engagement_comment_pts': 5,
    'engagement_response_pts': 5,
}

# ---------------------------------------------------------------------------
# Reputation Levels
# ---------------------------------------------------------------------------
REPUTATION_LEVELS = {
    'newcomer': (0, 49),
    'contributor': (50, 149),
    'trusted': (150, 299),
    'expert': (300, 499),
    'authority': (500, float('inf')),
}

# ---------------------------------------------------------------------------
# VeriPoint Site Configuration
# ---------------------------------------------------------------------------
SITE_NAME = 'VeriPoint'
SITE_TAGLINE = 'Verify Before You Trust.'
SITE_DESCRIPTION = (
    'An Evidence-Based Trust Platform that replaces star ratings '
    'with proof-backed credibility scoring.'
)
