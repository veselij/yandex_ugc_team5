# Decisions for new service (store analytics data)

## OLAP storage
Clickhouse chosen from other alternatives based on test results


## OLTP storage
Kafka chosen from other alternatives because it satisfies requirements:
- Atomicity
- Consistency
- Isolation
- Durability

## Web framework
FastAPI chosen from (FastAPI, Flask, Starlette, Django - as most popular), because it is async, with validation and dependency injection features
 