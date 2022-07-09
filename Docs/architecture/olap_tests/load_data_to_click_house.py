import uuid
from io import TextIOWrapper
from time import perf_counter
from typing import Generator

from clickhouse_driver import Client

CLICK_SELECTS = (
        """
        select distinct tt.user_id
        from test_db.test_table tt ;
        """,
        """
        select DISTINCT tt.film_id 
        from test_db.test_table tt ;
        """,
        """
        select tt.user_id , count(DISTINCT tt.film_id) watched
        from test_db.test_table tt 
        where tt.film_timestamp > 0
        group by tt.user_id 
        order by watched desc;
        """,
        """
        select res.film_id, AVG(res.watched) as avg_watch_time 
        from (
        select tt.film_id , tt.user_id , max(tt.film_timestamp) as watched
        from test_db.test_table tt 
        group by tt.film_id , tt.user_id) res
        group by res.film_id
        order by  avg_watch_time desc;
        """,
        """
        select res.film_id, count(res.watched) as top 
        from (
        select tt.film_id , tt.user_id , max(tt.film_timestamp) as watched
        from test_db.test_table tt 
        group by tt.film_id , tt.user_id) res
        group by res.film_id
        order by  top desc
        limit 5;
        """
)


def create_db(client: Client) -> None:
    client.execute('DROP DATABASE IF EXISTS test_db')
    client.execute('CREATE DATABASE IF NOT EXISTS test_db')
    client.execute('CREATE TABLE IF NOT EXISTS test_db.test_table (user_id UUID, film_id UUID, film_timestamp Int32) Engine=MergeTree() ORDER BY (user_id, film_id, film_timestamp)')


def read_data_in_chanks(file_obj: TextIOWrapper, lines_chank: int) -> Generator[list[list[int|str]], None, None]:
    result = []
    for index, data in enumerate(file_obj.readlines()):
        result.append([int(column) if i == 2 else uuid.UUID(column) for i, column in enumerate(data.split(';'))])
        if (index + 1) % lines_chank == 0:
            yield result
            result = []
    else:
        yield result


def insert_data(file_name: str, test_bath, client: Client) -> None:
    start = perf_counter()
    total_rows = 0
    with open(file_name, 'r') as fl:
        for rows in read_data_in_chanks(fl, test_bath):
            total_rows += len(rows)
            client.execute('INSERT INTO test_db.test_table (user_id, film_id, film_timestamp) VALUES', rows)
    stop = perf_counter()
    print(f'total rows {total_rows} batch size {test_bath} insert time {stop-start:.2f} seconds')


def select_data(client: Client, sql: str) -> None:
    start = perf_counter()
    result = client.execute(sql)
    stop = perf_counter()
    print(f'total rows selected {len(result)}  time {stop-start:.2f} seconds')




def main() -> None:
    chanks = (10, 100, 500, 1000, 10000, 100000)
    client = Client(host='localhost', port=19000)
    for chank in chanks:
        create_db(client)
        insert_data('test_data.csv', chank, client)
    for sql in CLICK_SELECTS:
        select_data(client, sql)
    

if __name__ == '__main__':
    main()
