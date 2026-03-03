# CEIT CMS Backend

FastAPI backend for CEIT CMS.

## Current Project Structure

```text
ceit-cms-backend/
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── f4a7fa96e76e_initial_migration.py
│       └── c8ab6cf878a8_backfill_article_status_timestamps.py
├── app/
│   ├── main.py
│   ├── api/v1/
│   │   ├── router.py
│   │   ├── dependencies.py
│   │   └── endpoints/
│   │       ├── auth.py
│   │       ├── article.py
│   │       └── upload.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── authz.py
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── scripts/
│   └── seed.py
├── requirements.txt
└── alembic.ini
```

## Local Setup (Backend Only)

1. Create Virtual Environment

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment

Linux/macOS:
```bash
cp .env.example .env
```

Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

Recommended local DB value in `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/ceit_cms
```

4. Start PostgreSQL

Linux/macOS (systemd):
```bash
sudo systemctl start postgresql
```

Windows (Service):
```powershell
net start postgresql-x64-17
```

If your service name differs, check it with:

```powershell
Get-Service *postgres*
```

5. Run migrations + seed

Linux/macOS:
```bash
./.venv/bin/alembic upgrade head
./.venv/bin/python scripts/seed.py
```

Windows:
```powershell
.venv\Scripts\alembic upgrade head
.venv\Scripts\python scripts\seed.py
```

6. Start API

Linux/macOS:
```bash
./.venv/bin/python -m app.main
```

Windows:
```powershell
.venv\Scripts\python -m app.main
```

## API URLs

- Base API: `http://127.0.0.1:8000/api/v1`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Auth Seed Accounts

Created by `scripts/seed.py`:

- `admin@ceit.edu` / `Admin123!`
- `ce.author@ceit.edu` / `Admin123!`
- `ee.author@ceit.edu` / `Admin123!`
- `it.author@ceit.edu` / `Admin123!`

## Start Full Workspace (Backend + Public + Admin)

Use separate terminals.

### Terminal 1 — PostgreSQL

Linux/macOS:
```bash
sudo systemctl start postgresql
```

Windows:
```powershell
net start postgresql-x64-17
```

### Terminal 2 — Backend

Linux/macOS:
```bash
cd /path/to/ceit-cms-backend
source .venv/bin/activate
./.venv/bin/alembic upgrade head
./.venv/bin/python scripts/seed.py
./.venv/bin/python -m app.main
```

Windows (replace with your local path):
```powershell
cd C:\path\to\ceit-cms-backend
.venv\Scripts\Activate.ps1
.venv\Scripts\alembic upgrade head
.venv\Scripts\python scripts\seed.py
.venv\Scripts\python -m app.main
```

### Terminal 3 — Public Frontend (`ceit-cms-frontend`)

Linux/macOS:
```bash
cd /pathh/to/ceit-cms-frontend
npm install
npm run dev

## or if using yarn

yarn install
yarn dev
```

Windows (PowerShell):
```powershell
cd C:\path\to\ceit-cms-frontend
npm install
npm run dev
```

### Terminal 4 — Admin Frontend (`BackendCMS`)

Linux/macOS:
```bash
cd /home/yue-os/Desktop/BackendCMS
npm install
npm run dev

## or if using yarn

yarn install
yarn dev
```

Windows (PowerShell):
```powershell
cd C:\path\to\BackendCMS
npm install
npm run dev

## or if using yarn

yarn install
yarn dev
```

## Important Behavior Notes

- Public endpoint `/api/v1/articles/` returns **approved** articles only.
- Publish from admin sets status to `approved`, so it appears on the public frontend.
- Archive from admin sets status to `archived`, so it disappears from public frontend.
