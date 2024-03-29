#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/dnlgby/dabert-app-api.git'

PROJECT_BASE_PATH='/usr/local/apps/dabert-rest-api'
PROJECT_MANAGE_PATH='/usr/local/apps/dabert-rest-api/dabert'


echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_MANAGE_PATH/env
python3 -m venv $PROJECT_MANAGE_PATH/env

# Install python packages
$PROJECT_MANAGE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_MANAGE_PATH/env/bin/pip install uwsgi==2.0.18

# Run migrations and collectstatic
cd $PROJECT_MANAGE_PATH
$PROJECT_MANAGE_PATH/env/bin/python manage.py migrate
$PROJECT_MANAGE_PATH/env/bin/python manage.py collectstatic --noinput

# Configure supervisor
echo "Setting supervisor..."
cp $PROJECT_BASE_PATH/deploy/supervisor_dabert_api.conf /etc/supervisor/conf.d/dabert_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart dabert_api

# Configure nginx
echo "Setting nginx..."
cp $PROJECT_BASE_PATH/deploy/nginx_dabert_api.conf /etc/nginx/sites-available/dabert_api.conf
# rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/dabert_api.conf /etc/nginx/sites-enabled/dabert_api.conf
systemctl restart nginx.service

echo "DONE! :)"
