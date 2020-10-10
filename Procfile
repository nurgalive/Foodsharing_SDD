release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn edudam.wsgi --log-file -
