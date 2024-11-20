
venv:
	@echo "creating the virtual_env mode"
	@python3 -m venv venv \
		&& /Users/amait-ou/Desktop/Transcendence/venv/bin/python3 -m pip install --upgrade pip

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

fclean: clean remove_migrations
	@echo "Full cleaning done!"

runserver:
	@echo "Running server..."
	@python3 Backend/manage.py runserver

shell:
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

createsuperuser:
	@echo "Creating superuser..."
	@python3 Backend/superuser_creation.py

