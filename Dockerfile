FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

# Saner Python & pip defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /workspace

# Install Python deps first (good cache hit rate)
# If you don't have requirements.txt, generate one or change to pyproject/lockfile install.
COPY requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -U pip && \
    pip install -r /tmp/requirements.txt

# Copy the app
COPY . .

# Ensure non-root user (provided by the Playwright base image) owns the workspace
RUN chown -R pwuser:pwuser /workspace
USER pwuser

# Default port for Django dev server (only used if you override CMD)
EXPOSE 8000

# Default behavior: run the test suite.
# To run Django instead, override at runtime:
# docker run --rm -p 8000:8000 IMAGE python manage.py runserver 0.0.0.0:8000
CMD ["bash", "-lc", "pytest -q"]
