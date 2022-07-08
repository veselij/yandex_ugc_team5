migrate:
	docker compose exec -w /code/migrations film_watch /bin/bash -c 'mongodb-migrate --url $$MONGODB_URL'

up:
	docker-compose -f mongodb.yml -f docker-compose.yml up -d

deploy-app:
	make up && make migrate

down:
	docker-compose -f mongodb.yml -f docker-compose.yml down --volumes
