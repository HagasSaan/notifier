![Python application](https://github.com/HagasSaan/notifier/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/HagasSaan/notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/HagasSaan/notifier)

# My Yet Another Scheduler Operator (MYASO)
Scheduler, working with messages, can consume messages from wherever you want and push it whatever you want.


TODO:

- [x] Покрыть тестами configuration
- [x] Вынести сортировку сообщений из Configuration.run(), создать отдельные фильтры, подключаемые к конфигурации
- [x] Допокрыть тестами github producer
- [x] Прикрутить консьюмер(telegram)
- [x] Прикрутить celery tasks
- [x] Собрать весь CI/CD пайплайн на Github Actions
- [x] Переделать фильтр SkipKeywords (вынести слова из конфигурации в фильтр)
- [ ] Прикрутить консьюмер(vk)
- [ ] Кастомизировать формат сообщений (текущий формат сделать как default)
- [ ] Сделать возможным в конфигурации множество продьюсеров и консьюмеров
- [x] Кастом продюсеры
- [x] Кастом консьюмер
- [x] Прикрутить Graphene
- [x] Прикрутить DRF
- [ ] На сладкое
    - [ ] Разобраться, как отдавать статичные файлы при DEBUG = false, отключить дебаг
    - [ ] Прикрутить Nginx
    - [ ] django-celery-results - поменять в зависимостях ссылку на гит на номер пакета
    - [ ] Зарезолвить все возникшие TODO
- [ ] Написать нормально ридми. Хотя бы раз в жизни
- [ ] Сделать документацию
    - [ ] Как написать свой продюсер\консьюмер
    - [ ] Как написать свой фильтр и подключить его
- [ ] Переименовать везде notifier в myaso
