#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Load tarot cards if not already loaded
python manage.py load_tarot_cards

# Collect static files
python manage.py collectstatic --no-input