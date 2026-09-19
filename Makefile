.PHONY: help install start stop clean

help:
	@echo "Commandes disponibles :"
	@echo "  make install    - Initialise l'environnement local (pre-commit)"
	@echo "  make start      - Lance les conteneurs (Airflow, dbt)"
	@echo "  make stop       - Arrête les conteneurs"

install:
	pip install pre-commit
	pre-commit install

start:
	docker-compose up -d

stop:
	docker-compose down
