from typing import Generator
import uuid
import random
import csv


def generate_fake_data() -> Generator[list, None, None]:
    users = [uuid.uuid4() for _ in range(10)]
    films = [uuid.uuid4() for _ in range(1000)]
    
    for user in users:
        for _ in range(20):
            film = random.choice(films)
            watch_time = random.randint(1, 7200)
            for second in range(watch_time):
                yield [user, film, second]


def write_to_file(filename: str) -> None:
    with open(filename, 'w') as fl:
        writer = csv.writer(fl, delimiter=';')
        for row in generate_fake_data():
            writer.writerow(row)


if __name__ == '__main__':
    write_to_file('test_data.csv')

