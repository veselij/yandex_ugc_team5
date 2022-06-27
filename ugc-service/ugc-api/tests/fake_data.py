import random
from uuid import uuid4

films_data = [
    {
        "film_id": str(uuid4()),
        "film_timestamp": random.randint(1, 1000),
    }
    for _ in range(10)
]
