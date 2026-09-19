.PHONY: help install start stop clean

help:
	@echo "Commandes disponibles :"
	@echo "  make install    - Initialise l'environnement local (pre-commit)"
	@echo "  make start      - Lance les conteneurs (Airflow, dbt)"
	@echo "  make stop       - Arrête les conteneurs"

install:
	pip install pre-commit
	# Installe le hook classique (pour le code terraform, python, dbt)
	pre-commit install
	# Installe le hook spécifique pour écouter les messages de commit
	pre-commit install --hook-type commit-msg

start:
	docker-compose up -d

stop:
	docker-compose down
