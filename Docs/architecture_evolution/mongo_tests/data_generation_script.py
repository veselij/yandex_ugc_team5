import json
import csv
import random
import uuid
from typing import Generator


def generate_fake_data() -> Generator[dict, None, None]:
    bookmarks = [uuid.uuid4() for _ in range(10000)]
    users = [uuid.uuid4() for _ in range(1000)]
    films = [uuid.uuid4() for _ in range(100000)]
    
    for bookmark in bookmarks:
        film = random.choice(films)
        user = random.choice(users)
        yield {"bookmark_id": bookmark, "user_id": user, "film_id": film}


def write_to_file(filename: str) -> None:
    with open(filename, 'w') as fl:
        writer = csv.writer(fl, delimiter=';')
        for row in generate_fake_data():
            writer.writerow(json.dump(row))


if __name__ == '__main__':
    write_to_file('test_data.csv')

