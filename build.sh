#!/bin/bash
# Build script for Render deployment

set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating standard Django superuser..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@hotel.com', 'admin123')"

echo "Creating custom customer-table admin user..."
python manage.py shell -c "from booking.models import User; User.objects.filter(email='admin@hotel.com').exists() or User.objects.create(user_id=(User.objects.order_by('-user_id').first().user_id + 1 if User.objects.exists() else 1), name='Admin User', email='admin@hotel.com', phone='0123456789', password='admin123')"

echo "Build completed successfully!"
