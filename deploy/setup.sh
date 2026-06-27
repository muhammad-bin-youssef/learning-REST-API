#!/usr/bin/env bash

set -e

PROJECT_GIT_URL='https://github.com/muhammad-bin-youssef/learning-REST-API.git'
PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'
PROJECT_SRC_PATH="$PROJECT_BASE_PATH/project"

export DEBIAN_FRONTEND=noninteractive
locale-gen en_GB.UTF-8

echo "Installing web server and database dependencies..."
apt-get update
# We stripped out all the heavy C-compilers. We only need these now:
apt-get install -y supervisor nginx git sqlite3 curl

echo "Installing uv (The blazing fast Python manager)..."
# Install uv so it is available globally in /usr/local/bin
curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh

echo "Setting up project directory..."
mkdir -p $PROJECT_BASE_PATH
if [ -d "$PROJECT_BASE_PATH/.git" ]; then
    rm -rf "$PROJECT_BASE_PATH"
fi
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

echo "Using uv to fetch Python 3.9 and build the environment instantly..."
# uv will seamlessly download a standalone Python 3.9 binary and create the venv
uv venv $PROJECT_BASE_PATH/env --python 3.9

echo "Installing dependencies with uv..."
# uv pip resolves and installs packages in a fraction of a second
uv pip install --python $PROJECT_BASE_PATH/env -r $PROJECT_BASE_PATH/requirements.txt
uv pip install --python $PROJECT_BASE_PATH/env gunicorn

echo "Running database migrations..."
$PROJECT_BASE_PATH/env/bin/python $PROJECT_SRC_PATH/manage.py migrate

echo "Configuring Server routing..."
cp $PROJECT_SRC_PATH/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart profiles_api

cp $PROJECT_SRC_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-enabled/profiles_api.conf
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf
systemctl restart nginx.service

echo "DONE! Go to sleep. :)"
