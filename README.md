![Python application](https://github.com/HagasSaan/notifier/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/HagasSaan/notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/HagasSaan/notifier)

# notifier
Notifier with producers and consumers


TODO:

- [x] Покрыть тестами configuration
- [x] Вынести сортировку сообщений из Configuration.run(), создать отдельные фильтры, подключаемые к конфигурации
- [x] Допокрыть тестами github producer
- [x] Прикрутить консьюмер(telegram)
- [ ] Прикрутить celery tasks
    - [x] Сделать запуск конфигурации асинхронной задачей
    - [ ] Сделать запуск конфигураций с определенным периодом ![Celery periodic tasks](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
- [ ] Собрать весь CI/CD пайплайн на Github Actions (желательно всё завернуть в контейнеры, даже тестирование на GA ![link](https://github.community/t/how-to-use-docker-compose-with-github-actions/16850/3))
    - [x] Прикрутить линтер
    - [x] Добавить выгрузку контейнера после тестов на Dockerhub
    - [x] Развернуть сервис вручную
    - [x] Получить манифесты для развёртывания каждого из сервисов по отдельности
    - [ ] Попробовать написать что-то деплоящее куда-то с GA
        - ![Конфигурирование AWS Credentials](https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions)
        - ![Создание контекста](https://github.com/marketplace/actions/kubernetes-set-context)
        - ![Запуск развёртывания приложения](https://github.com/marketplace/actions/kubernetes-set-context)
    - [ ] Сделать скрытие секретов в развертываемом проекте и их подключении через Vault
        - [ ] Переделать переменные в settings.py в os.environ.get()
        - [ ] Написать свой ConfigMap / Secrets для k8s
    - [ ] Сделать мониторинг на основе Sentry
        - [ ] ![Sentry Release](https://github.com/marketplace/actions/sentry-release)
- [ ] Переделать фильтр SkipKeywords (вынести слова из конфигурации в фильтр)
- [ ] Сделать приложение с MessageComponents
    - [ ] InternalMessage + ExternalMessage
    - [ ] Перенести MessageFilters в MessageComponents
- [ ] Прикрутить консьюмер(vk)
- [ ] Кастомизировать формат сообщений (текущий формат сделать как default)
- [ ] Кастом продюсеры, с различными параметрами авторизации, принимающие сообщения в формате
- [ ] Кастом консьюмер, 
- [ ] Подумать о добавлении скриптов через админку, и чтобы их можно было выполнять
    - [ ] Подумать про интерфейс
    - [ ] Подумать про безопасность таких настроек
    - [ ] Реализовать
- [ ] Подумать о применении проекта в качестве алерт-системы типа Balerter, которая будет чекать что-то скриптом, и пихать данные куда-то
- [ ] Прикрутить Graphene
    - [ ] Прикрутить авторизацию (OAuth 2.0)
    - [x] Просмотр возможных конфигураций, консьюмеров, продюсеров, их параметров
    - [x] Просмотр существующих конфигураций, консьюмеров, продюсеров, с сокрытием чувствительных данных
    - [ ] Создание объектов конфигураций, консьюмеров, продюсеров с помощью API
    - [ ] Прикрутить запуск конфигураций с помощью API
    - [ ] Включить линтер на файлы schema.py
    - [ ] Покрыть это всё тестами
    - [ ] Посмотреть в сторону ![оптимизации запросов](https://github.com/tfoxy/graphene-django-optimizer)
- [ ] Зарезолвить все возникшие TODO
- [ ] Написать нормально ридми. Хотя бы раз в жизни
- [ ] Сделать документацию
    - [ ] Как написать свой продюсер\консьюмер
    - [ ] Как написать свой фильтр и подключить его
    - [ ] Как добавлять свою доку в graphene для новых конфигураций
- [ ] Подумать в сторону разделени на микросервисы для горизонтальной масштабируемости
    - [ ] Event-based architecture?
    - [ ] Переписать core (configuration) на Rust?
