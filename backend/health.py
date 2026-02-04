#!/usr/bin/env python
"""Standalone health check script for Railway"""
import os
import sys
import django
from django.conf import settings
from django.http import HttpResponse

# Minimal Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def health_check(request):
    return HttpResponse("OK", status=200)

if __name__ == "__main__":
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()