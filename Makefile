rerun:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run python manage.py collectstatic --noinput
	poetry run black -S .
	poetry run isort .
	poetry run flake8
	#poetry run mypy .
	poetry run python manage.py runserver 0.0.0.0:8000

run:
	poetry run python manage.py runserver 0.0.0.0:8000

format:
	poetry run black -S .
	poetry run isort .

lint:
	poetry run flake8
	poetry run mypy .


shell:
	poetry run python manage.py shell -i ipython

migrations:
	poetry run python manage.py makemigrations

npc:
	poetry run python manage.py npc

load_data:
	poetry run python manage.py generate_fixtures
	poetry run python manage.py loaddata abilities
	poetry run python manage.py loaddata skills
	poetry run python manage.py loaddata class
	poetry run python manage.py loaddata race
	poetry run python manage.py loaddata weapon_types

messages:
	poetry run python manage.py makemessages --locale=ru
	poetry run python manage.py compilemessages