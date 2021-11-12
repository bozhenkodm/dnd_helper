rerun:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run black -S .
	poetry run isort .
# 	poetry run flake8
	poetry run python manage.py runserver 0.0.0.0:8000

run:
	poetry run python manage.py runserver 0.0.0.0:8000

format:
	poetry run black -S .
	poetry run isort .

shell:
	poetry run python manage.py shell -i ipython