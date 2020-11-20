![Python application](https://github.com/HagasSaan/notifier/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/HagasSaan/notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/HagasSaan/notifier)

# My Yet Another Scheduler Operator (MYASO)
Scheduler, working with messages, can consume messages from wherever you want and push it whatever you want.


TODO:

- [ ] Переделать USERNAME_KEY в ADDITIONAL_INFO_KEY, после чего уже там искать 'username', и прочие ключи
- [ ] Прикрутить консьюмер(vk)
- [ ] Прикрутить продюсер(redash) - на основе sql запроса генерация сообщения
- [ ] Кастомизировать формат сообщений (текущий формат сделать как default)
- [ ] На сладкое
    - [ ] Разобраться, как отдавать статичные файлы при DEBUG = false, отключить дебаг
    - [ ] Прикрутить Nginx
    - [ ] Зарезолвить все возникшие TODO
    - [ ] Дождаться Django Async ORM и переписать configuration.run()
- [ ] Написать нормально ридми. Хотя бы раз в жизни
- [ ] Сделать документацию
    - [ ] Как написать свой продюсер\консьюмер
    - [ ] Как написать свой фильтр и подключить его
    - [ ] Попросить пару людей почитать, понятно ли
    - [ ] Прочитать самому спустя полгода
- [ ] Переименовать везде notifier в myaso
