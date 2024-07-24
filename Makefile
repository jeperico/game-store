deps:
	poetry install

test: deps
	poetry run pytest -vvv

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

rundb:
	sudo docker compose -f docker-compose-dev.yml up -d --build

stopdb:
	sudo docker compose -f  docker-compose-dev.yml down

runserver:
	poetry run ./game-store/manage.py runserver 0.0.0.0:8000

createsuperuser:
	poetry run ./game-store/manage.py createsuperuser

migrate:
	poetry run ./game-store/manage.py migrate

makemigrations:
	poetry run ./game-store/manage.py makemigrations

makemigrations-merge:
	poetry run ./game-store/manage.py makemigrations --merge

