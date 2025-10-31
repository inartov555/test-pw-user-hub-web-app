"""
Static test data for users and common validation messages used in E2E tests.
"""

from __future__ import annotations


USERS = {
    "regular1": {"username": "test1", "password": "megaboss19", "role": "user"},
    "regular2": {"username": "test28", "password": "megaboss19", "role": "user"},
    "admin": {"username": "admin", "password": "changeme123", "role": "admin"},
}

VALIDATION = {
    "required_username": "Username is required",
    "required_password": "Password is required",
    "invalid_credentials": "Invalid username or password",
    "password_strength": "Password must be at least",
    "username_taken": "Username already exists",
}
