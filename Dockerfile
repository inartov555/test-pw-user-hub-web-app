FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /workspace
COPY pyproject.toml README.md pytest.ini /workspace/
RUN pip install -U pip && pip install -e .
COPY . /workspace
