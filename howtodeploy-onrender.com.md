# Deploy to Render

## Quick Start (Manual)

1. **Push repo to GitHub** and connect it to Render.

2. **Create a Web Service** on Render:
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn student_portal.wsgi`
   - **Plan**: Free or Starter

3. **Set environment variables** in Render dashboard (lowercase only — Render requires it):
   ```
   django_secret_key=<generate a long random key>
   debug=False
   production=True
   db_name=<Render PostgreSQL database>
   db_user=<Render PostgreSQL user>
   db_password=<Render PostgreSQL password>
   db_host=<Render PostgreSQL hostname>
   db_port=5432
   ```
   Uppercase names like `DB_NAME` also work (the code checks both).

4. **Create a PostgreSQL database** on Render and copy the connection details into the env vars above.

5. **Attach a Disk** (Render persistent disk) mounted at `/opt/render/project/src/media` for user-uploaded profile pictures. Without a disk, uploaded files will disappear after each deploy.

## Build Script

Create `build.sh` at repo root:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

Make it executable: `chmod +x build.sh`

## Troubleshooting

- **Static files 404**: Make sure `build.sh` runs `collectstatic`. WhiteNoise serves them — no extra config needed.
- **Media files lost after deploy**: Render's filesystem is ephemeral. Attach a persistent Disk or use cloud storage (S3, Cloudinary).
- **Database migrations fail**: Check `DB_*` env vars and ensure the Render PostgreSQL database is provisioned.
- **Build timeouts on free tier**: Keep `requirements.txt` lean. If the build exceeds 15 minutes, upgrade to Starter plan.
