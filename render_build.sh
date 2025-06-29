#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Load tarot cards if not already loaded
python manage.py shell < tarot_chatbot/load_cards.py

# Collect static files
python manage.py collectstatic --no-input