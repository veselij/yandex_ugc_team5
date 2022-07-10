``` mermaid
flowchart LR

user[user]
nginx(nginx)
fastapi(fastapi \n backend)
kafka(kafka)
clickhouse(clickhouse claster)

user -- film watch timestamp --> nginx
nginx --> fastapi
fastapi --> kafka
kafka -- clickhouse build-in ELT ---> clickhouse


```