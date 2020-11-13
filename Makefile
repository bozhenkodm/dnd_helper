rerun:
	python manage.py makemigrations; python manage.py migrate; black -S .; isort .; python manage.py runserver 0.0.0.0:8000

run:
	python manage.py runserver 0.0.0.0:8000

format:
	black -S .
	isort .

shell:
	python manage.py shell -i ipython