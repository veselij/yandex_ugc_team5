# Database selection

## Service requirements
1. Требования к скорости обработки данных = 200 мс
2. Горизонтальное масштабирование и репликация данных

## Структура данных
1. Bookmark
```
{
    bookmark_id,
    user_id,
    film_id
}
```

2. Likes
```
{
    like_id,
    user_id,
    film_id,
    value
}
```

3. Comment
```
{
    comment_id,
    user_id,
    film_id,
    text
}
```
## Первичный анализ

Рассмотрим 3 основных типа СУБД:
- реляционные
- колоночные
- документо-ориентированные

Наиболее популярным и производительным решением реляционных БД является Postgress. Но так как нам требуется горизонтальное масштабирование, организация репликации в Postgress становиться не тривиальной задачей. Так же в случае нормализации данных, возникают ситуации с меж-шардовыми джойнами, что приврет к проблемам с производительностью при росте данных и шардов. Если же деморализовать данные, то лучше использовать специализированные решения. Например Mongo DB.

Колоночные БД прежде всего преднеозначенные для аналитической работы с данными (являются OLAP системами хранения данных). Для ускорения работы с огромным количеством данных в таких системах используются механизмы оптимизации работы с индексами, как например в Clickhouse используются разреженные индексы. Отсюда возникает следующее ограничение, при большом количестве данных разреженность индекса может вырасти, в результате чего запросы на большие выборки данных будут работать быстрее. В то время как запросы на единичные строки начнут тормозить, так как по индексу находится только диапазон строк, а дальше идет сканирование всех строк в диапазоне, что может стать проблемой для нас, так как мы имеем ограничение на ответ в 200мс и все наши запросу будут касаться выборки нескольких строк. Также OLAP система кажется довольно избыточным решением в данном сервисе

Ввиду сказанного выше, наиболее оптимальным решением является использование документо-ориентированной СУБД. Наиболее популярной реализацией которого является Mongo DB.

Проведем несколько тестов подтверждающих, что производительность Mongo позволит обеспечить требуемые ограничения по скорости работы. Так как мы будем использовать шардирование и разносить по шардам данные пользователей на основе user_id. Таким образом все запросы связанные с одним пользователем будут выполнены на одном шарде. И конечная производительность будут определятся производительностью одного шарда. Проведем тесты только standalone Mongo

## Тесты

1. Тестовое HW
```
    Model Name: MacBook Air
    Model Identifier: MacBookAir10,1
    Chip: Apple M1
    Total Number of Cores: 8 (4 performance and 4 efficiency)
    Memory: 16 GB
    System Firmware Version: 7459.121.3
    OS Loader Version: 7459.121.3
```
2. Запуск БД
```
docker run -p 27017:27017 mongo
```
3. Загрузка данных
```
    total rows 1000000 batch size 1000 average insert time per batch 13.5 mseconds
```

4. Выборка данных
```
    total rows searched one by one 1000 times with average time 104.9 mseconds per one search
```
5. Выводы
Mongo обеспечивает необходимые требования по времени поиска и чтения данных.