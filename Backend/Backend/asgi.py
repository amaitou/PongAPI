"""
ASGI config for your_project_name project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'asgi' application.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

# Get the ASGI application
application = get_asgi_application()
