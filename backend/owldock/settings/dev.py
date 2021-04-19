from owldock.settings import *  # noqa
from owldock.dev.traceback import patch_exception_handler

import icecream

icecream.install()

patch_exception_handler()

DEBUG = True
DEV = True
ALLOWED_HOSTS[:] = ["*"]  # noqa
CORS_ALLOW_ALL_ORIGINS = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
INSTALLED_APPS.extend(  # noqa
    [
        "django_extensions",
        "django_fsm",  # for graph_transitions
        "django_seed",
    ]
)
if "INTERNAL_IPS" not in locals():
    INTERNAL_IPS = []
INTERNAL_IPS.append("192.168.1.3")  # noqa
MIDDLEWARE.extend(  # noqa
    [
        "app.middleware.process_exception.process_exception",
    ]
)
SHELL_PLUS_DJANGO_IMPORTS = False  # django.db.models.Case clashes with our Case
STATIC_ROOT = "static"
UI_DEV_MODE = False

DEBUG_TOOLBAR = False
if DEBUG_TOOLBAR:
    INSTALLED_APPS.insert(0, "debug_toolbar")  # noqa
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa

if UI_DEV_MODE:
    # In UI dev mode, the javascript client is running in a page served by a
    # node.js dev server; not Django. This is desirable, because then the UI
    # responds immediately when you edit javascript/css etc files. We will be
    # running the Django server also -- in order to handle the Ajax requests
    # made by the javascript. However, the Ajax requests made by the javascript
    # will have neither of the following things:
    # 1. The session_id cookie required to authenticate as a certain User
    # 2. The csrf_token required when handling POSTs
    #
    # To make the Ajax requests work, we do the following two things. Obviously,
    # the following code should never be executed in a production environment.

    # 1. Remove CSRF protection
    MIDDLEWARE.remove("django.middleware.csrf.CsrfViewMiddleware")  # noqa

    # 2. Automatically authenticate Ajax requests as an appropriate User.
    MIDDLEWARE.append(  # noqa
        "app.middleware.dev.insecurely_authenticate_as_requested_user",
    )

    LOGIN_REDIRECT_URL = "http://192.168.1.3:8080/portal/"
