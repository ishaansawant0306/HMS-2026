#!/usr/bin/env python
"""
Celery worker startup script for HMS
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run celery
from celery_config import celery_app

if __name__ == '__main__':
    # Pass all command line arguments to celery
    celery_app.start(sys.argv[1:])