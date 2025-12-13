release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && (python manage.py createsuperuser --noinput || true)
web: gunicorn followup_buddy.wsgi --log-file -