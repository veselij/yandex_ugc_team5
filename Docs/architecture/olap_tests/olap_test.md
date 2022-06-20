# OLAP test to chose solution

## Test HW
    Hardware Overview:
      Model Name: MacBook Air
      Model Identifier: MacBookAir10,1
      Chip: Apple M1
      Total Number of Cores: 8 (4 performance and 4 efficiency)
      Memory: 16 GB
      System Firmware Version: 7459.121.3
      OS Loader Version: 7459.121.3

## Test plan
1. generate test data (one csv file)
```
    "user_id": "", "film_id": "", "film_timestamp": ""
```
2. create database and table to store data
3. insert test data from csv file using butch and measure insert time:
    - butch size 10
    - butch size 100
    - butch size 500
    - butch size 1000
    - butch size 10000
    - butch size 100000
4. make select requests from database and measure execution time:
    - select uniq users
    - select uniq films
    - select number of film watched by user
    - select average watch time of film
    - select top 5 watched films

## ClickHouse
1. start server 
```
docker run -d -p 18123:8123 -p19000:9000 --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
```
3. create db and table
```
CREATE DATABASE IF NOT EXISTS test_db;
CREATE TABLE IF NOT EXISTS test_db.test_table (user_id UUID, film_id UUID, film_timestamp Int32) Engine=MergeTree() ORDER BY (user_id, film_id, film_timestamp);
```
3. insert data
```
total rows 644684 batch size     10 insert time 203.98 seconds
total rows 644684 batch size    100 insert time 26.64 seconds
total rows 644684 batch size    500 insert time 7.52 seconds
total rows 644684 batch size   1000 insert time 4.83 seconds
total rows 644684 batch size  10000 insert time 3.11 seconds
total rows 644684 batch size 100000 insert time 3.13 seconds
```
4. select data
```
total rows selected  10  time 0.02 seconds
total rows selected 183  time 0.01 seconds
total rows selected  10  time 0.01 seconds
total rows selected 183  time 0.01 seconds
total rows selected   5  time 0.01 seconds
```

## Vertica
1. start server 
```
docker run -p 5433:5433 jbfavre/vertica:latest
```
3. create db and table
```
CREATE SCHEMA IF NOT EXISTS test_db;
CREATE TABLE IF NOT EXISTS test_db.test_table (id IDENTITY, user_id UUID, film_id UUID, film_timestamp INTEGER);
```
3. insert data
```
total rows 644684 batch size     10 - crashes
total rows 644684 batch size    100 - crashes
total rows 644684 batch size    500 insert time 74.84 seconds
total rows 644684 batch size   1000 insert time 38.62 seconds
total rows 644684 batch size  10000 insert time 11.68 seconds
total rows 644684 batch size 100000 insert time 9.12 seconds
```
4. select data
```
total rows selected  10  time 0.12 seconds
total rows selected 183  time 0.09 seconds
total rows selected  10  time 0.22 seconds
total rows selected 183  time 0.17 seconds
total rows selected   5  time 0.16 seconds
```

## Comparison table

| operation |clickhouse, seconds|vertica, seconds|
|-----------|:---:|:---:|
|insert batch 10|204|crash|
|insert batch 100|27|crash|
|insert batch 500|8|75|
|insert batch 1000|5|39|
|insert batch 10000|3|12|
|insert batch 100000|3|9|
|select 1|0.02|0.12|
|select 2|0.01|0.09|
|select 3|0.01|0.22|
|select 4|0.01|0.17|
|select 5|0.01|0.16|