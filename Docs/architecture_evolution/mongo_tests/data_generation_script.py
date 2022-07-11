import json
import random
import uuid
from typing import Generator


def generate_fake_data() -> Generator[dict, None, None]:
    bookmarks = [uuid.uuid4() for _ in range(1000000)]
    users = [uuid.uuid4() for _ in range(100000)]
    films = [uuid.uuid4() for _ in range(100000)]

    for bookmark in bookmarks:
        film = random.choice(films)
        user = random.choice(users)
        yield {"bookmark_id": str(bookmark), "user_id": str(user), "film_id": str(film)}


def write_to_file(filename: str) -> None:
    with open(filename, "w") as fl:
        for row in generate_fake_data():
            fl.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    write_to_file("test_data.csv")
