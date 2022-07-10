
``` mermaid
flowchart LR

user[user]
nginx(nginx)
fastapi(fastapi \n backend)
kafka(kafka)
clickhouse(clickhouse claster)

logstash(logstash)
style logstash fill: pink
elasticsearch(elasticsearch)
style elasticsearch fill: pink
kibana(kibana)
style kibana fill: pink
mongo(cluster mongo)
style mongo fill: pink
beats(beats)
style beats fill: pink



user -- film watch timestamp --> nginx
user -- user likes, comments, bookmarks --> nginx
nginx --> fastapi
fastapi -- film watch timestamp --> kafka
kafka -- clickhouse build-in ELT ---> clickhouse

fastapi -- user likes, comments, bookmarks --> mongo
fastapi --> logstash
nginx --> beats --> logstash --> elasticsearch --> kibana

```