FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

# Saner Python & pip defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /test

# Install Python deps first (good cache hit rate)
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=.cache/pip \
    python -m pip install -U pip && \
    pip install -r requirements.txt

# Copy the app
COPY . .

# Ensure non-root user (provided by the Playwright base image) owns the workspace
RUN chown -R pwuser:pwuser /test
USER pwuser

# Default behavior: run the test suite.
CMD ["bash", "-lc", "pytest -q"]
