FROM python:3.10-slim as build

WORKDIR /app
RUN pip install pdm
COPY pyproject.toml pyproject.lock* ./
RUN pdm install --prod --no-editable

FROM python:3.10-slim

WORKDIR /app
RUN useradd -m -u 1000 bot
COPY --from=build /app/.venv /app/.venv
COPY src ./src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER bot
CMD ["python", "-m", "antijob_bot"]
