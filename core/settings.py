import os
from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool)

API_KEY = config("API_KEY")
NIKITA_LOGIN = config("NIKITA_LOGIN")
NIKITA_PASSWORD = config("NIKITA_PASSWORD")
NIKITA_SENDER = config("NIKITA_SENDER")
NIKITA_TEST = config("NIKITA_TEST")
SECRET_KEY_SMS = config("SECRET_KEY_SMS")

MERCHANT_ID = config("MERCHANT_ID")
PAY_SECRET_KEY = config("PAY_SECRET_KEY")
PG_SUCCESS_URL = config("PG_SUCCESS_URL")
PG_FAILURE_URL = config("PG_FAILURE_URL")
PG_BACK_LINK = config("PG_BACK_LINK")

AUTH_USER_MODEL = "user.CustomUser"

ALLOWED_HOSTS = ["*"]

MY_APPS = [
    "apps.chat",
    "apps.home",
    "apps.my_house",
    "apps.user",
    "apps.userprofile",
    "apps.blogs",
    "apps.payment",
    "apps.notifications"
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "django_ckeditor_5",
    "reportlab",
    "channels",
    "drf_spectacular",
    "django_filters"
]

INSTALLED_APPS = (
        [
            "daphne",
            "jazzmin",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ]
        + MY_APPS
        + THIRD_PARTY_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = 'core.asgi.application'
WSGI_APPLICATION = 'core.wsgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "language": "en",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
    },
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Library Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Library",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Library",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "books/img/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the library",

    # Copyright on the footer
    "copyright": "Acme Library Ltd",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string


    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu


    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "apps.blogs.news", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "custom_jazzmin/main.css",
    "custom_js": "custom_jazzmin/main.js",
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Bishkek"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'TSJ',
    'DESCRIPTION': 'ready application programming Interface',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config("SECRET_KEY"),
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
}
