#!/bin/bash
set -e

case $1 in
    build)
        docker build -f Dockerfile -t queue:latest .
        ;;
    dev)
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
        ;;

    start)
        docker compose up -d
        ;;
    stop)
        docker compose down
        ;;
esac