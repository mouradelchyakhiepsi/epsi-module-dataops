.PHONY: help install start stop clean

# Définition des chemins vers l'environnement virtuel
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PRECOMMIT = $(VENV)/bin/pre-commit

help:
	@echo "Commandes disponibles :"
	@echo "  make install    - Initialise l'environnement local (venv + pre-commit)"
	@echo "  make start      - Lance les conteneurs (Airflow, dbt)"
	@echo "  make stop       - Arrête les conteneurs"

install:
	@echo "Création de l'environnement virtuel Python..."
	python3 -m venv $(VENV)
	@echo "Installation de pre-commit dans le venv..."
	$(PIP) install pre-commit
	@echo "Configuration des hooks Git..."
	$(PRECOMMIT) install
	$(PRECOMMIT) install --hook-type commit-msg
	@echo "✅ Terminé ! (Note: le venv est géré automatiquement par Makefile pour pre-commit)"

start:
	docker-compose up -d

stop:
	docker-compose down
