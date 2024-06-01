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

MY_APPS = ["apps.chat", "apps.home", "apps.my_house", "apps.user", "apps.userprofile", "apps.blogs", "apps.payment"]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "django_ckeditor_5",
    "reportlab",
    "channels",
    "drf_spectacular",
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
            "hosts": [('127.0.0.1', 6379)],
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

# JAZZMIN_SETTINGS = {
#     "site_title": "TSJ",
#     "site_header": "TSJ",
#     "site_brand": "TSJ",
#     "site_logo_classes": "img-square",
#     "user_avatar": None,
#     "search_model": ["auth.User", "auth.Group"],
#     "topmenu_links": [
#         {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
#         {
#             "name": "Support",
#             "url": "https://github.com/farridav/django-jazzmin/issues",
#             "new_window": True,
#         },
#     ],
#     "usermenu_links": [
#         {
#             "name": "Support",
#             "url": "https://github.com/farridav/django-jazzmin/issues",
#             "new_window": True,
#         }
#     ],
#     "show_sidebar": True,
#     "navigation_expanded": True,
#     "hide_apps": [],
#     "hide_models": [],
#     "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
#     "custom_links": {
#         "books": [
#             {
#                 "name": "Make Messages",
#                 "url": "make_messages",
#                 "icon": "fas fa-comments",
#                 "permissions": ["books.view_book"],
#             }
#         ]
#     },
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "auth.Group": "fas fa-users",
#     },
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-circle",
#     "related_modal_active": False,
#     "custom_css": None,
#     "custom_js": None,
#     "use_google_fonts_cdn": True,
#     "show_ui_builder": False,
#     "changeform_format": "horizontal_tabs",
#     "changeform_format_overrides": {
#         "auth.user": "collapsible",
#         "auth.group": "vertical_tabs",
#     },
# }


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

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
    "site_title": "TSJ",
    "site_header": "TSJ",
    "navigation_expanded": True,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "related_modal_active": False,
    "new_buttons_location": "bottom",
    "show_export_csv": True,
    "show_export_json": True,
    "show_related_modal": True,
    "changeform_format_overrides": {
        "flat": "collapsible",
        "news": "vertical_tabs",
        "request": "vertical_tabs",
        "request_votenews": "vertical_tabs",
    },
    "collapsible_sidebar": True,
    "default_cascade": False,
    "cascade": False,
    "nav_menu_icon": "fa-fw fas fa-bars",
    "search_bar_icon": "fa-fw fas fa-search",
    "changeform_format": "horizontal_tabs",
    "form_horizontal": False,
    "actions_sticky_top": True,
    "actions_sticky_bottom": True,
    "actions_extra_top": True,
    "actions_extra_bottom": True,
    "changeform_format_overrides": {
        "auth.user": "horizontal_tabs",
        "auth.group": "horizontal_tabs",
    },
    "show_ui_builder": True,
    "ui_builder_function": "jazzmin.views.dynamic_list_filter",
    "ui_builder_exclude": [
        "django.contrib.auth.models.Group",
        "django.contrib.auth.models.User",
    ],
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
