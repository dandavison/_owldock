from typing import List

from owldock.settings import *

ALLOWED_HOSTS[:] = ["*"]

UI_DEV_MODE = True

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
    MIDDLEWARE.remove("django.middleware.csrf.CsrfViewMiddleware")

    # 2. Automatically authenticate Ajax requests as an appropriate User.
    MIDDLEWARE.append(
        "app.middleware.dev.auto_authenticate_according_to_requested_endpoint",
    )
