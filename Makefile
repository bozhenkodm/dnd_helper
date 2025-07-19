rerun:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run python manage.py collectstatic --noinput
	poetry run black -S .
	poetry run isort .
	poetry run flake8
	#poetry run mypy .
	DJANGO_RUNSERVER_HIDE_WARNING=true poetry run python manage.py runserver 0.0.0.0:8000

run:
	DJANGO_RUNSERVER_HIDE_WARNING=true poetry run python manage.py runserver 0.0.0.0:8000

serve:
	poetry run gunicorn dnd_helper.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120

serve-dev:
	poetry run gunicorn dnd_helper.wsgi:application --bind 127.0.0.1:8000 --workers 2 --reload --timeout 60

format:
	poetry run black -S .
	poetry run isort .

lint:
	poetry run flake8
	poetry run mypy .
	#poetry run vulture .


shell:
	poetry run python manage.py shell -i ipython --verbosity=2

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

test:
	cp db.sqlite3 /tmp/db_test.sqlite3
	poetry run pytest -vv