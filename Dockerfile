FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1 AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd --gid 10001 labtrack \
    && useradd --uid 10001 --gid 10001 --create-home labtrack
COPY --chown=labtrack:labtrack app app
COPY --chown=labtrack:labtrack frontend frontend
COPY --chown=labtrack:labtrack migrations migrations
COPY --chown=labtrack:labtrack alembic.ini .
RUN mkdir /app/data && chown labtrack:labtrack /app/data
USER labtrack
EXPOSE 8000
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS test
USER root
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY --chown=labtrack:labtrack tests tests
COPY --chown=labtrack:labtrack pyproject.toml .
USER labtrack
CMD ["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"]

FROM base AS runtime
