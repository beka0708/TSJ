import os
from datetime import timedelta
from pathlib import Path
from decouple import config
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

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
            "unfold",  # before django.contrib.admin
            "unfold.contrib.filters",  # optional, if special filters are needed
            "unfold.contrib.forms",  # optional, if special form elements are needed
            "unfold.contrib.inlines",  # optional, if special inlines are needed
            "unfold.contrib.import_export",  # optional, if django-import-export package is used
            "unfold.contrib.guardian",  # optional, if django-guardian package is used
            "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
            'django_static_jquery_ui',
            'django_tabbed_changeform_admin',
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

from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "TCЖ",
    "SITE_HEADER": "TCЖ",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",  # Символ из набора иконок
    "SHOW_HISTORY": True,  # Показать/скрыть кнопку "History"
    "SHOW_VIEW_ON_SITE": True,  # Показать/скрыть кнопку "View on site"

    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
        "secondary": {
            "50": "240 248 255",
            "100": "225 245 254",
            "200": "205 230 253",
            "300": "175 210 251",
            "400": "130 180 249",
            "500": "85 150 247",
            "600": "51 120 235",
            "700": "34 100 210",
            "800": "33 90 180",
            "900": "28 75 150",
            "950": "7 50 100",
        },
    },

    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },

    "SIDEBAR": {
        "show_search": True,  # Поиск по приложениям и моделям
        "show_all_applications": False,  # Выпадающий список со всеми приложениями и моделями
        "navigation": [
            {
                "title": _(""),
                "separator": True,  # Разделитель
                "items": [
                    {
                        "title": _("Главная"),
                        "icon": "dashboard",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": "chat.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },

                ],
            },
            {
                "title": _(""),
                "separator": True,  # Разделитель
                "items": [

                    {
                        "title": _("Пользователи"),
                        "icon": "people",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:user_customuser_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Новости"),
                        "icon": "article",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:blogs_news_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Чаты"),
                        "icon": "chat",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:chat_room_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("ТСЖ"),
                        "icon": "apartment",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_tsj_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Камеры"),
                        "icon": "videocam",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:my_house_camera_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Уведомление"),
                        "icon": "notifications",  # Иконка из набора: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:notifications_toadminnotification_changelist"),
                        "badge": "0",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },

    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),  # Путь к изображению фона на странице входа
        "redirect_after": lambda request: reverse_lazy("admin:index"),  # Перенаправление после входа
    },

    "STYLES": [
        lambda request: static("css/custom-style.css"),  # Подключение кастомных стилей
    ],

    "SCRIPTS": [
        lambda request: static("js/custom-script.js"),  # Подключение кастомных скриптов
    ],
    "DASHBOARD_CALLBACK": "apps.blogs.views.dashboard_callback"
}


def badge_callback(request):
    return 3
