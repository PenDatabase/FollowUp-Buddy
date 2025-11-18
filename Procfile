release: python manage.py makemigrations && python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn followup_buddy.wsgi --log-file -