/home/pi/.local/bin/gunicorn --certfile=certs/certificate.crt --keyfile=certs/private.key  -w 4  --bind 0.0.0.0:5000 wsgi:app
