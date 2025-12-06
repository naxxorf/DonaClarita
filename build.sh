#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
# We need to navigate to where manage.py is
cd hostalDonaClarita
python manage.py collectstatic --noinput
python manage.py migrate
