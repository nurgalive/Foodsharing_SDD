release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn edudam.wsgi --timeout 120 --keep-alive 10 --log-file -
