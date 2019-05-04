#!/usr/bin/env sh
# cria os arquivos de log e começa a rastreá-los
touch /logs/gunicorn.log
touch /logs/gunicorn-access.log
tail -n 0 -f /logs/gunicorn*.log &

python manage.py collectstatic --no-input

sleep 60

exec gunicorn api_sinarodo.wsgi:application \
    --name api_expedicao \
    --bind 0.0.0.0:8080 \
    --workers 5 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/gunicorn-access.log
"$@"
