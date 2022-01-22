from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="!!!SET DJANGO_SECRET_KEY!!!",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Security Settings for Staging and Production
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", True)
SECURE_BROWSER_XSS_FILTER = env.bool("DJANGO_SECURE_BROWSER_XSS_FILTER", True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", True)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', 31536000)
SECURE_REDIRECT_EXEMPT = env.list('DJANGO_SECURE_REDIRECT_EXEMPT', default=[])
SECURE_SSL_HOST = env.str('DJANGO_SECURE_SSL_HOST', None)
SECURE_SSL_REDIRECT = env.bool("DJANGO_SESSION_COOKIE_SECURE", True)
SECURE_PROXY_SSL_HEADER = env.tuple("DJANGO_SECURE_PROXY_SSL_HEADER",
    default=('HTTP_X_FORWARDED_PROTO', 'https')
)