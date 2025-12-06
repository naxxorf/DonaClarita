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
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='hostalDonClarita').exists() or User.objects.create_superuser('hostalDonClarita', 'admin@example.com', 'administracion')"