import pymongo.mongo_client as mongo
from pymongo.collection import Collection
import json
from io import TextIOWrapper
from time import perf_counter
from typing import Generator


test_ids: set[dict] = set()

def read_data_in_chanks(file_obj: TextIOWrapper, lines_chank: int) -> Generator[list[list[str]], None, None]:
    result = []
    for index, data in enumerate(file_obj.readlines()):
        result.append(json.load(data))
        if (index + 1) % lines_chank == 0:
            test_ids.add(data)
            yield result
            result = []
    else:
        yield result


def insert_data(file_name: str, test_bath, client: Collection) -> None:
    start = perf_counter()
    total_rows = 0
    with open(file_name, 'r') as fl:
        for rows in read_data_in_chanks(fl, test_bath):
            total_rows += len(rows)
            client.insert_many(rows)
    stop = perf_counter()
    print(f'total rows {total_rows} batch size {test_bath} insert time {stop-start:.2f} seconds')


def select_one(row: dict, client: Collection) -> float:
    start = perf_counter()
    client.find_one(row)
    stop = perf_counter()
    return stop - start


def main():
    client = mongo.MongoClient('localhost', 27017)
    collection = client["test_db"]["test_collection"]
    insert_data("test_data.csv", 1000, collection)

    total_time = 0
    for id in test_ids:
        total_time += select_one(id, collection)
    print(f"total rows searched one by one {len(test_ids)} with average time {total_time/len(test_ids):.2f} seconds")


if __name__ == "__main__":
    main()