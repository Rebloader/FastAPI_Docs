#!/bin/bash

celery -A src.tasks:celery worker --loglevel=INFO --pool=solo &

alembic revision --autogenerate -m 'create tables'
alembic upgrade head

uvicorn main:app --reload --host 0.0.0.0 --port 8000