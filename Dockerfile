FROM python:3.10-slim AS build

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN pip install pdm
COPY pyproject.toml pyproject.lock* ./
RUN pdm install --prod --no-editable

FROM python:3.10-slim

WORKDIR /app
RUN useradd -m -u 1000 bot
COPY --from=build /app/.venv /app/.venv
COPY src ./src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

USER bot
CMD ["python", "-m", "antijob_bot"]
