![Python application](https://github.com/HagasSaan/notifier/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/HagasSaan/notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/HagasSaan/notifier)

# My Yet Another Scheduler Operator (MYASO)
Scheduler, working with messages, can consume messages from wherever you want and push it whatever you want.


TODO:

- [x] Покрыть тестами configuration
- [x] Вынести сортировку сообщений из Configuration.run(), создать отдельные фильтры, подключаемые к конфигурации
- [x] Допокрыть тестами github producer
- [x] Прикрутить консьюмер(telegram)
- [ ] Прикрутить celery tasks
    - [x] Сделать запуск конфигурации асинхронной задачей
    - [ ] Сделать запуск конфигураций с определенным периодом [Celery periodic tasks](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
        - [Заблокировано несовместимостью Celery 5.* и django-celery-beat](https://github.com/celery/django-celery-beat/pull/365)
    - [ ] Прикрутить отображение таски 
        - [Заблокировано несовместимостью Celery 5.* и django-celery-results](https://github.com/celery/django-celery-results/pull/158)
- [ ] Собрать весь CI/CD пайплайн на Github Actions
    - [x] Прикрутить линтер
    - [x] Добавить выгрузку контейнера после тестов на Dockerhub
    - [x] Развернуть сервис вручную
    - [x] Получить манифесты для развёртывания каждого из сервисов по отдельности
    - [ ] Попробовать написать что-то деплоящее куда-то с GA
        - [Конфигурирование AWS Credentials](https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions)
        - [Создание контекста kubernetes](https://github.com/marketplace/actions/kubernetes-set-context)
        - [Запуск развёртывания приложения kubernetes](https://github.com/marketplace/actions/kubernetes-set-context)
    - [ ] Сделать скрытие секретов в развертываемом проекте и их подключении через Vault
        - [x] Переделать переменные в settings.py в os.environ.get()
        - [ ] Написать свой ConfigMap / Secrets для k8s
    - [x] Сделать мониторинг на основе Sentry
        - [x] [Sentry Release](https://github.com/marketplace/actions/sentry-release)
- [x] Переделать фильтр SkipKeywords (вынести слова из конфигурации в фильтр)
- [ ] Прикрутить консьюмер(vk)
- [ ] Кастомизировать формат сообщений (текущий формат сделать как default)
- [x] Кастом продюсеры
- [x] Кастом консьюмер
- [ ] Прикрутить Graphene
    - [x] Просмотр возможных конфигураций, консьюмеров, продюсеров, их параметров
    - [ ] Создание объектов конфигураций, консьюмеров, продюсеров с помощью API
    - [ ] Прикрутить запуск конфигураций с помощью API
    - [ ] Покрыть это всё тестами
    - [ ] Посмотреть в сторону [оптимизации запросов](https://github.com/tfoxy/graphene-django-optimizer)
- [ ] Прикрутить DRF
    - [x] Просмотр возможных конфигураций, консьюмеров, продюсеров, их параметров
    - [ ] Создание объектов конфигураций, консьюмеров, продюсеров с помощью API
    - [x] Прикрутить запуск конфигураций с помощью API
    - [ ] Покрыть это всё тестами
- [ ] Зарезолвить все возникшие TODO
- [ ] Написать нормально ридми. Хотя бы раз в жизни
- [ ] Сделать документацию
    - [ ] Как написать свой продюсер\консьюмер
    - [ ] Как написать свой фильтр и подключить его
    - [ ] Как добавлять свою доку в graphene для новых конфигураций
- [ ] Подумать в сторону разделени на микросервисы для горизонтальной масштабируемости
    - [ ] Event-based architecture?
    - [ ] Переписать core (configuration) на Rust?
- [ ] Переименовать везде notifier в myaso
