FROM python:3.10-buster
WORKDIR /
RUN pip install pdm
COPY . .
RUN pdm install --prod --no-lock --no-editable
CMD pdm run antijob_bot
