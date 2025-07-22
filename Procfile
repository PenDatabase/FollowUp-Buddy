
web: python manage.py migrate && web: python manage.py collectstatic --noinput && gunicorn followup_buddy.wsgi:application --bind 0.0.0.0:$PORT --log-level debug --access-logfile - --error-logfile -
