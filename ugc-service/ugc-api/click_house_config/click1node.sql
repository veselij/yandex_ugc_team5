CREATE DATABASE IF NOT EXISTS shard;
CREATE DATABASE IF NOT EXISTS replica;
CREATE TABLE IF NOT EXISTS shard.film_watch_status_queue (user_id UUID, film_id UUID, film_timestamp Int32) ENGINE=Kafka() SETTINGS kafka_broker_list = 'broker:9092', kafka_topic_list = 'movies', kafka_group_name = 'group_movies', kafka_format = 'JSONEachRow';
CREATE TABLE IF NOT EXISTS shard.film_watch_status (user_id UUID, film_id UUID, film_timestamp Int32) ENGINE=ReplicatedMergeTree('/clickhouse/tables/shard1/film_watch_status', 'replica_1') ORDER BY (user_id, film_id, film_timestamp);
CREATE TABLE IF NOT EXISTS replica.film_watch_status (user_id UUID, film_id UUID, film_timestamp Int32)ENGINE=ReplicatedMergeTree('/clickhouse/tables/shard2/film_watch_status', 'replica_2') ORDER BY (user_id, film_id, film_timestamp);
CREATE TABLE default.film_watch_status (user_id UUID,film_id UUID,film_timestamp Int32) ENGINE=Distributed('company_cluster','',film_watch_status,rand());
CREATE MATERIALIZED VIEW shard.film_watch_status_view TO shard.film_watch_status AS SELECT user_id, film_id, film_timestamp FROM shard.film_watch_status_queue;
