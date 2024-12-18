
runserver:
	@echo "Running server..."
	@python3 Backend/manage.py runserver

venv:
	@echo "creating the virtual_env mode"
	@python3 -m venv venv

requirements:
	@echo "Requirements are being installed ..."
	@pip3 install -r requirements.txt


remove_pycache:
	@echo "Removing __pycache__ directories..."
	@find . -name '__pycache__' -exec rm -rf {} +

remove_pyc:
	@echo "Removing .pyc files..."
	@find . -name '*.pyc' -exec rm -f {} +

clean: remove_pycache remove_pyc
	@echo "Cleaning done!"

fclean: clean
	@echo "Full cleaning done!"

shell:
	@echo "Running python shell..."
	@python3 Backend/manage.py shell

migrate: makemigrations
	@echo "Migrating..."
	@python3 Backend/manage.py migrate

makemigrations:
	@echo "Making migrations..."
	@python3 Backend/manage.py makemigrations

flush:
	@echo "Flushing..."
	@python3 Backend/manage.py flush --no-input

createsuperuser:
	@echo "Creating superuser..."
	@python3 Backend/superuser_creation.py

