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
- [ ] Собрать весь CI/CD пайплайн на Github Actions (желательно всё завернуть в контейнеры, даже тестирование на GA)
- [x] Прикрутить линтер
- [ ] Построить нормальный пайплайн выгрузки хоть куда-то
- [ ] Сделать скрытие секретов в репозитории и их подключении через Vault
- [ ] Зарезолвить все возникшие TODO
- [ ] Написать нормально ридми. Хотя бы раз в жизни
- [ ] Сделать мониторинг на основе Sentry
- [ ] Кастом продюсер (url+port+login+pass etc), который отдает сообщения в требуемом формате
- [ ] Кастом консьюмер, который принимает сообщения в определенном формате