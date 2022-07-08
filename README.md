# Sprint 8 UGC
## Назначение 
1. Данный сервис предназначен для сбора данных о просмотрах фильмов пользователями кинотеатра
2. Так же осуществляется сохранение полученных данных в аналитическом хранилище.
3. В рамках данной работы так же были протестированы два аналитических хранилища и [выбран лучший вариант](Docs/architecture/olap_tests/)

## Компоненты сервиса
1. Веб сервис на основе [fastapi](https://fastapi.tiangolo.com). End point /api/v1/ принимающий POST запросы от пользователя с установленным параметром Bearer jwt_token в Header запроса в формате: 
```
{
    film_id: UUID,
    film_timestamp: int
}
```
2. Kafka сервис для сохранения данных полученных в end point.
3. Clickhouse кластер с 2 репликами и 2 распределенными нодами на 4 хостах для сохранения аналитической информации о просмотренных фильмах для последующего анализа данных.
4. Перенос данных их Kafka в Clickhouse организован по средствам встроенных в clickhouse механизмов работы с Kafka. На каждой из реплик созданы локальные таблицы для чтения данных из kafka и вставки в другую локальную таблицы, на основе которых создана одна распределенная таблица
5. Для проверки валидности запросов от пользователей используется сервис Auth. Результаты проверок токенов сохраняются в redis БД для минимизации запросов к Auth сервису.

## Запуск проекта
Проект запускается в среде докер по средством двух docker-compose файлов: 
1. docker-compose.yml - запускает сервис состоящий из всех компонент(Kafka, ClickHouse, Redis, Film_wath_service). команды для запуска: 
```
склонировать проект в {папку}
cd {папка}
cd ugc-service/ugc-api
cp .env.sample .env
make deploy-app
```
2. docker-compose.dev.yml - дополнительно к основным сервисам выполняется тест, который проверяет, что запросы пользователей сохраняются в Clickhouse: 
```
склонировать проект в {папку}
cd {папка}
cd ugc-service/ugc-api
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up

посмотреть логи тестов
docker log film_watch_test
```

## Участники проекта
1. team-lead [veseij](https://github.com/veselij)
2. Разработчик [AmirbegKK](https://github.com/AmirbegKK)
3. Разработчик [Che1](https://github.com/Che1)


## Changelog
1. 24.06.2022: 
    - first release, main service
2. 27.06.2022:
    - add readme.md
    - changed extraction of user_id from client request to extraction from user request access token