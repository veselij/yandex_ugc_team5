#!/bin/sh
echo "Start gunicorn server"
python3 -m gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 start_server:app

exec "$@"
