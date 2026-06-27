#!/usr/bin/env bash

set -e

PROJECT_GIT_URL='https://github.com/muhammad-bin-youssef/learning-REST-API.git'
PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'
PROJECT_SRC_PATH="$PROJECT_BASE_PATH/project"

# Set Ubuntu Language non-interactively
export DEBIAN_FRONTEND=noninteractive
locale-gen en_GB.UTF-8

# Install Python, SQLite3 and pip
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite3 python3-pip supervisor nginx git build-essential

mkdir -p $PROJECT_BASE_PATH
# Delete directory if it already exists to prevent git clone failure
if [ -d "$PROJECT_BASE_PATH/.git" ]; then
    rm -rf "$PROJECT_BASE_PATH"
fi
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

python3 -m venv $PROJECT_BASE_PATH/env

# Upgrade baseline packaging tools
$PROJECT_BASE_PATH/env/bin/pip install --upgrade pip setuptools wheel

# Install requirements along with Gunicorn and the cgi fix for Python 3.14
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install gunicorn legacy-cgi

# Run migrations from the project subdirectory
$PROJECT_BASE_PATH/env/bin/python $PROJECT_SRC_PATH/manage.py migrate

# Setup Supervisor to run our gunicorn process
cp $PROJECT_SRC_PATH/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart profiles_api

# Setup nginx to make our application accessible
cp $PROJECT_SRC_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-enabled/profiles_api.conf
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf
systemctl restart nginx.service

echo "DONE! :)"
