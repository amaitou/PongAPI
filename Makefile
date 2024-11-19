

remove_pycache:
	@echo "Removing __pycache__ directories..."
	@find . -name '__pycache__' -exec rm -rf {} +

remove_pyc:
	@echo "Removing .pyc files..."
	@find . -name '*.pyc' -exec rm -f {} +

runserver:
	@echo "Running server..."
	@python3 Backend/manage.py runserver

python_shell:
	@echo "Running python shell..."
	@python3 Backend/manage.py shell

migrate:
	@echo "Migrating..."
	@python3 Backend/manage.py migrate

makemigrations:
	@echo "Making migrations..."
	@python3 Backend/manage.py makemigrations

flush:
	@echo "Flushing..."
	@python3 Backend/manage.py flush --no-input