#!/usr/bin/env python3
"""
Migration script for production deployment
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/opt/render/project/src')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sc_courts_app.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
