

# Write a comprehensive deployment troubleshooting guide as a markdown file

guide = """# Django REST API Deployment Troubleshooting Guide

## Server Environment
- **Instance**: AWS EC2 t3.micro (Ubuntu 26.04 LTS - resolute)
- **Public IP**: 13.41.76.186
- **Instance ID**: i-00d2ac1539b907a7b (omarchy-api)
- **Security Group**: launch-wizard-1 (sg-06a0758ee8953eabc)
- **VPC**: vpc-0ef6add2049609660

---

## Problem 1: uWSGI Compilation Failure

### Symptom
```
error: passing argument 2 of 'signal' from incompatible pointer type
```

### Root Cause
- Python 3.14 (system default) + GCC 14 treat incompatible function pointers as fatal errors
- uWSGI 2.0.21 C source code uses outdated signal handler declarations (`void (*)(void)` instead of `void (*)(int)`)

### Solution
**Abandon uWSGI. Use Gunicorn instead.**

```bash
# In setup.sh, replace:
pip install uwsgi==2.0.21
# With:
pip install gunicorn
```

---

## Problem 2: Python 3.14 Incompatibility with Django 2.2

### Symptom
```
ModuleNotFoundError: No module named 'cgi'
```

### Root Cause
- Django 2.2 depends on `cgi` module (removed in Python 3.14)
- `django.utils.six.moves` also fails on Python 3.14

### Solution
**Use `uv` to install Python 3.9 alongside system Python 3.14.**

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh

# Create venv with Python 3.9
uv venv /usr/local/apps/profiles-rest-api/env --python 3.9

# Install dependencies
uv pip install --python /usr/local/apps/profiles-rest-api/env -r requirements.txt
uv pip install --python /usr/local/apps/profiles-rest-api/env gunicorn
```

**CRITICAL**: Do NOT attempt `sudo apt remove python3` — it breaks the entire Ubuntu system.

**CRITICAL**: Do NOT use deadsnakes PPA on Ubuntu 26.04 — it does not provide Python 3.9 (requires libssl<3).

---

## Problem 3: Working Directory Deleted During Git Clone

### Symptom
```
fatal: Unable to read current working directory: No such file or directory
```

### Root Cause
Running setup script from inside `/usr/local/apps/profiles-rest-api` while the script contains `rm -rf "$PROJECT_BASE_PATH"`

### Solution
Always run deployment scripts from home directory:
```bash
cd ~
curl -sL https://raw.githubusercontent.com/.../setup.sh | sudo bash -
```

---

## Problem 4: ModuleNotFoundError - WSGI Path

### Symptom
```
ModuleNotFoundError: No module named 'profiles_api'
```

### Root Cause
- `wsgi.py` located at: `/usr/local/apps/profiles-rest-api/project/project/wsgi.py`
- Supervisor config points to `profiles_api.wsgi:application` (wrong module name)

### Solution
```bash
# Find actual wsgi.py location
find /usr/local/apps/profiles-rest-api/project/ -name "wsgi.py"
# Returns: /usr/local/apps/profiles-rest-api/project/project/wsgi.py

# Fix Supervisor config
sudo sed -i 's/profiles_api.wsgi:application/project.wsgi:application/' \
    /etc/supervisor/conf.d/profiles_api.conf

# Also fix directory path
directory = /usr/local/apps/profiles-rest-api/project
```

---

## Problem 5: Nginx Config File Missing

### Symptom
```
open() "/etc/nginx/sites-enabled/profiles_api.conf" failed (2: No such file or directory)
```

### Root Cause
- `setup.sh` copies from `$PROJECT_SRC_PATH/deploy/` but nginx config is at repo root: `$PROJECT_BASE_PATH/deploy/`
- `cp` command fails silently, symlink points to non-existent file

### Solution
```bash
# Copy from correct location
sudo cp /usr/local/apps/profiles-rest-api/deploy/nginx_profiles_api.conf \
    /etc/nginx/sites-available/profiles_api.conf

# Create symlink
sudo ln -sf /etc/nginx/sites-available/profiles_api.conf \
    /etc/nginx/sites-enabled/profiles_api.conf

# Remove default
sudo rm -f /etc/nginx/sites-enabled/default
```

---

## Problem 6: Nginx Upstream Port Mismatch

### Symptom
Nginx fails or returns 502 Bad Gateway

### Root Cause
- Nginx config: `proxy_pass http://127.0.0.1:9000/`
- Gunicorn binds to: `127.0.0.1:8000`

### Solution
```bash
sudo sed -i 's/127.0.0.1:9000/127.0.0.1:8000/' \
    /etc/nginx/sites-available/profiles_api.conf
sudo nginx -t
sudo systemctl restart nginx
```

---

## Problem 7: AWS Security Group Blocking HTTP

### Symptom
```
ERR_CONNECTION_REFUSED from browser
```
Nginx IS listening on :80 (confirmed via `ss -tlnp`)

### Root Cause
Security Group only allows SSH (22) and HTTPS (443), not HTTP (80)

### Solution
In AWS Console:
1. EC2 → Instances → select instance
2. Security → Security Groups → launch-wizard-1
3. Inbound Rules → Edit → Add Rule:
   - Type: HTTP
   - Port: 80
   - Source: 0.0.0.0/0
4. Save

---

## Problem 8: Django ALLOWED_HOSTS

### Symptom
```
DisallowedHost at /
Invalid HTTP_HOST header: '13.41.76.186'
```

### Root Cause
`ALLOWED_HOSTS` only contains old IP: `['ec2-16-171-238-229...', '127.0.0.1']`

### Solution
```bash
sudo sed -i "s/ALLOWED_HOSTS = \[/ALLOWED_HOSTS = ['13.41.76.186', /" \
    /usr/local/apps/profiles-rest-api/project/project/settings.py
sudo supervisorctl restart profiles_api
```

**Note**: Elastic IP not configured. If instance stops, IP changes and must update both:
- AWS Security Group rules (if IP-based)
- Django ALLOWED_HOSTS
- Nginx server_name (if set)

---

## Problem 9: Static Files Not Loading (CSS/JS)

### Symptom
Browsable API loads without styling — plain HTML only

### Root Cause
`collectstatic` outputs to wrong directory due to relative `STATIC_ROOT`

### Current State
- `STATIC_ROOT = 'static/'` (relative to where manage.py is executed)
- Running from `/home/ubuntu` → files go to `/home/ubuntu/static`
- Nginx looks at `/usr/local/apps/profiles-rest-api/project/static/`

### Solution
```bash
# Run collectstatic from project directory
cd /usr/local/apps/profiles-rest-api/project
sudo /usr/local/apps/profiles-rest-api/env/bin/python manage.py collectstatic --noinput

# Verify
ls -la /usr/local/apps/profiles-rest-api/project/static/

# Ensure Nginx points to correct location
# In /etc/nginx/sites-available/profiles_api.conf:
location /static {
    alias /usr/local/apps/profiles-rest-api/project/static;
}
```

---

## Final Working Configuration

### Directory Structure
```
/usr/local/apps/profiles-rest-api/
├── deploy/
│   ├── setup.sh
│   ├── nginx_profiles_api.conf
│   └── supervisor_profiles_api.conf
├── project/
│   ├── manage.py
│   ├── project/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── profile_api/
│   └── db.sqlite3
└── env/          (uv-managed Python 3.9 venv)
```

### Supervisor Config (/etc/supervisor/conf.d/profiles_api.conf)
```ini
[program:profiles_api]
command = /usr/local/apps/profiles-rest-api/env/bin/gunicorn project.wsgi:application --bind 127.0.0.1:8000
directory = /usr/local/apps/profiles-rest-api/project
user = root
autostart = true
autorestart = true
umask = 022
stdout_logfile = /var/log/supervisor/profiles_api.log
stderr_logfile = /var/log/supervisor/profiles_api_err.log
```

### Nginx Config (/etc/nginx/sites-available/profiles_api.conf)
```nginx
server {
    listen 80 default_server;

    location /static {
        alias /usr/local/apps/profiles-rest-api/project/static;
    }

    location / {
        proxy_pass        http://127.0.0.1:8000/;
        proxy_set_header  Host                $host;
        proxy_set_header  X-Real-IP           $remote_addr;
        proxy_set_header  X-Forwarded-For     $remote_addr;
        proxy_set_header  X-Forwarded-Proto   $scheme;
        proxy_redirect    off;
    }
}
```

### Key Commands
```bash
# Check all services
sudo supervisorctl status profiles_api
sudo systemctl status nginx --no-pager
sudo ss -tlnp | grep -E ':80|:8000'

# View logs
sudo supervisorctl tail profiles_api stderr
sudo cat /var/log/supervisor/profiles_api_err.log
sudo cat /var/log/nginx/error.log

# Restart everything
sudo supervisorctl restart profiles_api
sudo systemctl restart nginx

# Test nginx config
sudo nginx -t
```

---

## Deployment Script (setup.sh) - FINAL VERSION

```bash
#!/usr/bin/env bash
set -e

PROJECT_GIT_URL='https://github.com/muhammad-bin-youssef/learning-REST-API.git'
PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'
PROJECT_SRC_PATH="$PROJECT_BASE_PATH/project"

export DEBIAN_FRONTEND=noninteractive
locale-gen en_GB.UTF-8

echo "Installing dependencies..."
apt-get update
apt-get install -y supervisor nginx git sqlite3 curl

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh

echo "Setting up project..."
mkdir -p $PROJECT_BASE_PATH
if [ -d "$PROJECT_BASE_PATH/.git" ]; then
    rm -rf "$PROJECT_BASE_PATH"
fi
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

echo "Creating Python 3.9 environment..."
uv venv $PROJECT_BASE_PATH/env --python 3.9

echo "Installing packages..."
uv pip install --python $PROJECT_BASE_PATH/env -r $PROJECT_BASE_PATH/requirements.txt
uv pip install --python $PROJECT_BASE_PATH/env gunicorn

echo "Collecting static files..."
cd $PROJECT_SRC_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

echo "Running migrations..."
$PROJECT_BASE_PATH/env/bin/python manage.py migrate

echo "Configuring Supervisor..."
cp $PROJECT_BASE_PATH/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart profiles_api

echo "Configuring Nginx..."
cp $PROJECT_BASE_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-enabled/profiles_api.conf
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf
systemctl restart nginx

echo "DONE!"
```

---

## Lessons Learned

1. **Never fight compiler errors with legacy C packages** — switch to pure-Python alternatives (Gunicorn vs uWSGI)
2. **Never remove system Python** — use isolated environments (uv, pyenv) instead
3. **Always verify file paths** — `find` before assuming directory structure
4. **Always run destructive scripts from safe directory** — `cd ~` before `rm -rf`
5. **Check AWS Security Groups first** — when browser can't connect but services are running
6. **Use `uv` for Python version management** — faster, cleaner, no deadsnakes PPA dependency hell
7. **Django `ALLOWED_HOSTS` must include current public IP** — updates needed when IP changes
8. **Run `collectstatic` from project directory** — relative paths resolve differently based on CWD
"""

with open('/mnt/agents/output/django-deployment-troubleshooting.md', 'w') as f:
    f.write(guide)

print("File saved successfully!")
print(f"Length: {len(guide)} characters")
