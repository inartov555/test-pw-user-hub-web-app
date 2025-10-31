"""Lightweight proxy to call Django manage commands from tests.

Used by data seeding scripts. Assumes current working dir is repository root with manage.py.
"""
from __future__ import annotations
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "project.settings"))
django.setup()
