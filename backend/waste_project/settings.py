from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-waste-prediction-backend"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "prediction",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "waste_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "waste_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================
# LOGIN CONFIGURATION
# ============================================
LOGIN_REDIRECT_URL = "/admin/"
LOGIN_URL = "/admin/login/"

# ============================================
# JAZZMIN BRANDING & CUSTOMIZATION
# ============================================

JAZZMIN_SETTINGS = {
    "site_title": "Waste System",
    "site_header": "Waste System Admin Panel",
    "site_brand": "Waste System",
    "welcome_sign": "Welcome to Waste Management System",
    "copyright": "2026 Waste Management System. All rights reserved.",
    "login_logo": "/static/images/logo.svg",
    "logo": "/static/images/logo.svg",
    "logo_alt": "Waste System Logo",
    "site_logo_max_height": 60,
    "user_avatar": None,
    "use_gravatar": False,
    "search_model": ["auth.User"],
    "show_ui_builder": False,
    "get_settings_callable": None,
    "navigation": {
        "vertically_collapsible": True,
        "collapsed": False,
    },
    "show_search": True,
    "search_model": ["auth.User", "auth.Group"],
    "icons": {
        "auth": "fas fa-users",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
        "prediction": "fas fa-trash",
    },
    "default_icon": "fas fa-circle",
    "side_panel_position": "left",
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small": False,
    "footer_small": False,
    "body_small": False,
    "sign_in_template": None,
    "welcome_sign": "Welcome to Waste Management System",
    "login_logo_max_height": 100,
    "navbar_color": "#2E7D32",
    "navbar_text_color": "#FFFFFF",
    "primary_color": "#2E7D32",
    "secondary_color": "#66BB6A",
    "accent": "#43A047",
    "darker_accent": "#1B5E20",
    "sidebar_width": "260px",
    "content_padding": "20px 20px 20px 0",
    "search_input_attrs": {
        "placeholder": "Search...",
        "class": "search-input",
    },
    "admin_title": "Waste System Admin",
    "admin_logo": "/static/images/logo.svg",
}

# ============================================
# CORS CONFIGURATION FOR REACT FRONTEND
# ============================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

CORS_ALLOW_CREDENTIALS = True
