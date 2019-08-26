#!/usr/bin/env bash

set -e

PROJECT_MANAGE_PATH='/usr/local/apps/dabert-rest-api/dabert'

git pull
$PROJECT_MANAGE_PATH/env/bin/python manage.py migrate
$PROJECT_MANAGE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart dabert_api

echo "DONE! :)"
