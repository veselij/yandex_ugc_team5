import json
from io import TextIOWrapper
from time import perf_counter
from typing import Generator

import pymongo.mongo_client as mongo
from pymongo.collection import Collection

test_ids: list[dict] = []


def read_data_in_chanks(
    file_obj: TextIOWrapper, lines_chank: int
) -> Generator[list[list[str]], None, None]:
    result = []
    for index, data in enumerate(file_obj.readlines()):
        result.append(json.loads(data))
        if (index + 1) % lines_chank == 0:
            test_ids.append(json.loads(data))
            yield result
            result = []
    else:
        yield result


def insert_data(file_name: str, test_bath, client: Collection) -> None:
    total_rows = 0
    total_time = 0
    with open(file_name, "r") as fl:
        for rows in read_data_in_chanks(fl, test_bath):
            if rows:
                total_rows += len(rows)
                start = perf_counter()
                client.insert_many(rows)
                stop = perf_counter()
                total_time += stop - start

    print(
        f"total rows {total_rows} batch size {test_bath} average insert time {total_time/(total_rows/test_bath)*1000:.1f} mseconds"
    )


def select_one(row: dict, client: Collection) -> float:
    start = perf_counter()
    client.find_one(row)
    stop = perf_counter()
    return stop - start


def main():
    client = mongo.MongoClient("localhost", 27017)
    collection = client["test_db"]["test_collection"]
    insert_data("test_data.csv", 1000, collection)

    total_time = 0
    for id in test_ids:
        total_time += select_one(id, collection)
    print(
        f"total rows searched one by one {len(test_ids)} with average time {total_time/len(test_ids)*1000:.1f} mseconds"
    )


if __name__ == "__main__":
    main()
