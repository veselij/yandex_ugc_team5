# General Tasks
## Features requirements
- User watch history
- User bookmark films
- User film end watch timestamp
- Film user likes
- Film user comments

## Todo
1. Prepare solution architecture (block and sequence schemes):
    - AS IS
    - TO BE
2. After selecting architecture make ADR record:
    - what is the decision
    - decision context
    - estimated alternative approaches
3. Configure Kafka and make async service to receive data from user device
4. Choose 3 OLAP providers and prepare comparison summary:
    - read/write speeds benchmark
    - db schemas
    - scripts to load or generate fake data in db
    - other  
    Candidates:
        - Apache Spark
        - ClickHouse
        - Vertica
        - Amazon Web services
5. ETL from Kafka to chosen OLAP storage (ClickHouse):
    - Проверьте, что схема данных вашего аналитического хранилища поддерживает возможность находить самые просматриваемые фильмы и понимать, какие фильмы не досматривают до конца
    - Продумайте возможность непрерывной работы ETL-процесса так, чтобы он был толерантен к сбоям источника данных и хранилища.
    - Так как поток данных ожидается непрерывным нужно проверить, что ваше приложение не «течёт». То есть нужно внедрить средства мониторинга памяти приложения.
