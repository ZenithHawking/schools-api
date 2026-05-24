# UniAPI

> Open API for Vietnamese universities, colleges, faculties & campuses.

**API:** https://apihoavan.xyz/openapi/

**Docs:** https://apihoavan.xyz/openapi/docs

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Usage

### Base URL

```
https://apihoavan.xyz/openapi
```

### Endpoints

```bash
# List schools (with pagination)
GET /api/v1/schools?limit=50&skip=0

# Search by name or code
GET /api/v1/schools?search=bach+khoa

# Filter by type and country
GET /api/v1/schools?type=public&country=VN

# School detail
GET /api/v1/schools/{school_id}

# Faculties
GET /api/v1/faculties
GET /api/v1/schools/{school_id}/faculties

# Campuses
GET /api/v1/schools/{school_id}/campuses
```

### Response Example

```json
{
  "id": "hcmus",
  "code": "QTD",
  "name": "Truong Dai hoc Khoa hoc Tu nhien",
  "type": "public",
  "country": "VN",
  "contact": {
    "website": "https://www.hcmus.edu.vn",
    "email": "dhkhtn@hcmus.edu.vn"
  },
  "campuses": [],
  "faculties": []
}
```

### Rate Limits

| Endpoint | Limit |
|----------|-------|
| `GET /schools` | 100/min |
| `GET /schools/{id}` | 200/min |
| `GET /faculties` | 50/min |
| `POST/PUT/DELETE` | 10/min |

---

## Development

```bash
git clone https://github.com/ZenithHawking/schools-api.git
cd schools-api

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python scripts/import_data.py
uvicorn app.main:app --reload --port 8000
```

### Refresh Government School Data

```bash
python scripts/fetch_government_public_schools.py
python scripts/import_data.py
```

### Tech Stack

- **FastAPI** 0.109.0
- **SQLAlchemy** 2.0
- **SQLite**
- **Uvicorn**

---

## Data

All JSON files in `data/` are auto-imported by `scripts/import_data.py`.

You can add new files like `data/hanoi-schools.json`, `data/hcm-schools.json`, etc.

### Schema

| Table | Fields |
|-------|--------|
| **schools** | id, code, name, type, country, contact, verified |
| **faculties** | id, school_id, name, code, programs |
| **campuses** | id, school_id, name, address, is_main |

### Add a School

```json
{
  "id": "school-slug",
  "code": "ABC",
  "name": "Full school name",
  "type": "public",
  "country": "VN",
  "contact": { "website": "https://...", "email": "..." },
  "campuses": [{ "name": "Main", "address": "...", "is_main": true }],
  "faculties": [{ "id": "fac-slug", "name": "...", "code": "XX", "programs": [] }],
  "metadata": { "verified": false, "created_at": "2026-01-26", "updated_at": "2026-01-26" }
}
```

---

## Deploy

```bash
git clone https://github.com/ZenithHawking/schools-api.git
cd schools-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/import_data.py
```

### Systemd Service

```ini
[Unit]
Description=UniAPI
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/schools-api
Environment="PATH=/path/to/schools-api/venv/bin"
ExecStart=/path/to/schools-api/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 5001
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable schools-api
sudo systemctl start schools-api
```

---

## Contributing

1. Fork & clone
2. Create branch: `git checkout -b add-school-abc`
3. Add data to `data/*.json`
4. Test locally
5. Open a Pull Request

---

## License

MIT License - Free to use.

---

**Issues:** [GitHub Issues](https://github.com/ZenithHawking/schools-api/issues)

Made by Zenith
