#!/usr/bin/env bash
set -o errexit

exec gunicorn student_portal.wsgi --workers=4 --timeout=120 --access-logfile=- --error-logfile=-
