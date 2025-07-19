# D&D Helper

A Django-based application designed to assist Dungeon Masters in creating and managing D&D 4th Edition content.

## Features

- **NPC Creation**: Generate non-player characters with powers and equipment
- **Power Management**: Create and manage character powers with image-based parsing
- **Name Generator**: Generate random race names for NPCs
- **Encounter Management**: Track and manage game encounters
- **Grid Maps**: Create and manage battle maps
- **Item Management**: Handle magical items and equipment

## Requirements

- Python 3.12+
- Django 5.x
- Gunicorn (production server)
- SQLite (default database)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dnd_helper
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Run database migrations:
```bash
poetry run python manage.py migrate
```

4. Create a superuser (optional):
```bash
poetry run python manage.py createsuperuser
```

5. Load initial data (optional):
```bash
make load_data
```

6. Start the server:
```bash
# Development with Django's built-in server
make run

# Development with Gunicorn (recommended)
make serve-dev

# Production with Gunicorn
make serve
```

## Usage

Access the application at `http://127.0.0.1:8000/` after starting the development server.

### Admin Interface

Visit `http://127.0.0.1:8000/admin/` to access the Django admin interface for managing data.

## Development

### Make Commands

The project includes a Makefile with convenient commands:

- `make run`: Start the Django development server
- `make serve`: Start production server with Gunicorn (4 workers)
- `make serve-dev`: Start development server with Gunicorn (2 workers, auto-reload)
- `make rerun`: Full development cycle (migrations, static files, formatting, linting, and server start)
- `make format`: Format code using Black and isort
- `make lint`: Run linting with Flake8 and MyPy
- `make test`: Run the test suite
- `make migrations`: Generate new database migrations
- `make shell`: Start Django shell with IPython
- `make npc`: Run NPC management command
- `make load_data`: Load initial fixtures into the database
- `make messages`: Generate and compile translation messages

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

Run individual commands:
```bash
make format
make lint
make test
```

Or run the full development cycle:
```bash
make rerun
```

### Pre-commit Hooks

Pre-commit hooks are configured to run automatically before commits. Install them with:
```bash
poetry run pre-commit install
```

## Project Structure

- `base/`: Core application with models, views, and utilities
- `generator/`: NPC and content generation functionality
- `encounters/`: Encounter management
- `items/`: Item and equipment management
- `printer/`: Map and printable content management
- `features/`: Additional game features
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `media/`: User-uploaded files

## Testing

Run tests using pytest:
```bash
poetry run pytest
```

## License

This project is intended for personal and educational use in D&D gaming sessions.
