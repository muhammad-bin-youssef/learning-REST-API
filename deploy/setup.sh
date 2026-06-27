#!/usr/bin/env bash

set -e

PROJECT_GIT_URL='https://github.com/muhammad-bin-youssef/learning-REST-API.git'
PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'
PROJECT_SRC_PATH="$PROJECT_BASE_PATH/project"

# Set Ubuntu Language non-interactively
export DEBIAN_FRONTEND=noninteractive
locale-gen en_GB.UTF-8

echo "Adding deadsnakes repository for legacy Python support..."
apt-get update
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

echo "Installing dependencies (including Python 3.9)..."
apt-get install -y python3.9 python3.9-dev python3.9-venv sqlite3 supervisor nginx git build-essential

mkdir -p $PROJECT_BASE_PATH
# Delete directory if it already exists to prevent git clone failure
if [ -d "$PROJECT_BASE_PATH/.git" ]; then
    rm -rf "$PROJECT_BASE_PATH"
fi
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Force the virtual environment to build explicitly using Python 3.9
python3.9 -m venv $PROJECT_BASE_PATH/env

# Upgrade baseline packaging tools inside the environment
$PROJECT_BASE_PATH/env/bin/pip install --upgrade pip setuptools wheel

# Install production dependencies safely under Python 3.9
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install gunicorn

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
