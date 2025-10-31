FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy

# Saner Python & pip defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Copy the app
COPY . /tests

WORKDIR /tests

RUN --mount=type=cache,target=.cache/pip \
    python -m pip install -U pip && \
    pip install -r requirements.txt

# Ensure non-root user (provided by the Playwright base image) owns the workspace
RUN chown -R pwuser:pwuser /tests
USER pwuser

# Default behavior: run the tests suite with a virtual display
CMD ["bash", "-lc", "xvfb-run -a pytest -q"]
