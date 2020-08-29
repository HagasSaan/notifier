![Python application](https://github.com/HagasSaan/notifier/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/HagasSaan/notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/HagasSaan/notifier)

# notifier
Notifier with producers and consumers


TODO:
- [x] Покрыть тестами configuration
- [x] Допокрыть тестами github producer
- [x] Прикрутить консьюмер(telegram)
- [x] Прикрутить celery tasks
- [ ] Прикрутить DRF (или graphene) для вызова тасок через API (Через OAuth 2.0)
- [ ] Прикрутить консьюмер(vk)
- [ ] Добавить режим, когда конфигурацию можно вызвать через API
- [ ] Собрать весь CI/CD пайплайн на Github Actions (желательно всё завернуть в контейнеры, даже тестирование на GA ![link](https://github.community/t/how-to-use-docker-compose-with-github-actions/16850/3))
- [x] Прикрутить линтер
- [ ] Построить нормальный пайплайн выгрузки хоть куда-то
- [ ] Сделать скрытие секретов в репозитории и их подключении через Vault
- [ ] Зарезолвить все возникшие TODO
- [ ] Написать нормально ридми. Хотя бы раз в жизни
- [ ] Сделать мониторинг на основе Sentry
- [ ] Кастомизировать формат сообщений (текущий формат сделать как default)
- [ ] Кастом продюсер (url+port+login+pass etc)
- [ ] Кастом консьюмер