# antijob_bot

[![pre-commit](https://github.com/antijob/antijob_bot/workflows/pre-commit/badge.svg)](https://github.com/antijob/antijob_bot/actions?query=workflow%3Apre-commit)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![License: AGPL-3.0](https://img.shields.io/github/license/antijob/antijob_bot)](https://github.com/antijob/antijob_bot/blob/main/COPYING)

---

Телеграм-бот для [antijob.net](https://antijob.net/).

## Запуск

- Локально (compose): `docker compose up --build`
- Продакшн (swarm): `docker stack deploy --compose-file docker-compose.prod.yml antijob_bot`

Для запуска на том же swarm-узле, где работает `antijob/reviews-bot`,
используется ограничение `node.labels.service == ${SWARM_NODE_SERVICE_LABEL}`.
По умолчанию: `SWARM_NODE_SERVICE_LABEL=antijob_bot_reviews`.

## Лицензия
antijob_bot выпущен под GNU Affero General Public License v3.0. Смотрите [COPYING](COPYING) для полных условий лицензирования.
