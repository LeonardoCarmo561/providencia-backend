"""
ASGI config for Providencia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import environ
from pathlib import Path
from django.core.asgi import get_asgi_application

env = environ.Env(
    CONFIG=(str, 'local')
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

CONFIG = env('CONFIG')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'Providencia.settings.{CONFIG}')

application = get_asgi_application()
