"""Example Django data seeder for multi-column sorting.

Replace `YourModel` and fields with the actual project models.
If the project provides a custom management command already, you can remove this file and call that.
"""
from __future__ import annotations
from .manage_proxy import *  # noqa
from django.db import transaction
from django.apps import apps

APP_LABEL = "app"
MODEL_NAME = "User"  # change to your model

def _records():
    last_names = ["Brown", "Clark", "Davis", "Evans", "Foster"]
    roles = ["viewer", "editor", "admin"]
    for i in range(60):
        yield {
            "first_name": f"Alex-{i:02}",
            "last_name": last_names[i % len(last_names)],
            "email": f"alex{i:02}@example.com",
            "role": roles[i % len(roles)],
        }

@transaction.atomic
def main():
    model = apps.get_model(APP_LABEL, MODEL_NAME)
    model.objects.filter(email__startswith="alex").delete()
    model.objects.bulk_create([model(**r) for r in _records()])
    print("Seeded multi-column sorting dataset.")

if __name__ == "__main__":
    main()
