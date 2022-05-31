release: python manage.py migrate
web: gunicorn fantasyfootballapp.wsgi
web: python manage.py collectstatic --no-input; gunicorn fantasyfootballapp.wsgi --log-file - --log-level debug