#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
import sys

if __name__ == '__main__':
    # If WEBSITE_HOSTNAME is defined as an environment variable, then we're running
    # on Azure App Service and should use the production settings.
    settings_module = "python_webapp_django.settings" #"python_webapp_django.production" if 1 else 'python_webapp_django.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
