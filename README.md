# 🎓 Schools API

> Open API cho các trường đại học, cao đẳng tại Việt Nam

🌐 **API:** https://apihoavan.xyz/openapi/

📖 **Docs:** https://apihoavan.xyz/openapi/docs

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Sử dụng API

### Base URL
```
https://apihoavan.xyz/openapi
```

### Endpoints

```bash
# Danh sách trường
GET /api/v1/schools

# Chi tiết trường
GET /api/v1/schools/{school_id}

# Tìm kiếm
GET /api/v1/schools?search=bách+khoa

# Lọc theo loại
GET /api/v1/schools?type=public&country=VN

# Danh sách khoa
GET /api/v1/faculties

# Khoa của một trường
GET /api/v1/schools/{school_id}/faculties
```

### Response Example

```json
[
  {
    "id": "hcmus",
    "code": "QTD",
    "name": "Trường Đại học Khoa học Tự nhiên",
    "type": "public",
    "country": "VN",
    "contact": {
      "website": "https://www.hcmus.edu.vn",
      "email": "dhkhtn@hcmus.edu.vn"
    },
    "campuses": [...],
    "faculties": [...]
  }
]
```

---

## 💻 Development

### Quick Start

```bash
# Clone repo
git clone https://github.com/ZenithHawking/schools-api.git
cd schools-api

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Import data
python scripts/import_data.py

# Run server
uvicorn app.main:app --reload --port 8000
```

### Tech Stack

- **FastAPI** 0.109.0
- **SQLAlchemy** 2.0
- **SQLite** (có thể dùng PostgreSQL)
- **Uvicorn**

---

## 🤝 Đóng góp

### Cách 1: Edit trên GitHub (Dễ nhất)

1. Vào file: [`data/schools.json`](https://github.com/ZenithHawking/schools-api/blob/main/data/schools.json)
2. Click nút **✏️ Edit**
3. Thêm thông tin trường theo format
4. Click **"Propose changes"** → Tạo Pull Request

### Cách 2: Fork & PR

```bash
# Fork repo → Clone về máy
git clone https://github.com/YOUR_USERNAME/schools-api.git

# Tạo branch mới
git checkout -b add-school-abc

# Thêm data vào data/*.json
# Commit & push
git add data/
git commit -m "Add: Trường ABC"
git push origin add-school-abc

# Tạo Pull Request trên GitHub
```

### Template trường mới

```json
{
  "id": "school-slug",
  "code": "ABC",
  "name": "Tên trường đầy đủ",
  "description": "Mô tả ngắn gọn",
  "type": "public",
  "country": "VN",
  "contact": {
    "website": "https://...",
    "email": "contact@..."
  },
  "campuses": [
    {
      "name": "Cơ sở chính",
      "address": "Địa chỉ đầy đủ",
      "is_main": true
    }
  ],
  "faculties": [
    {
      "id": "faculty-slug",
      "name": "Tên khoa",
      "code": "XX",
      "programs": ["Ngành 1", "Ngành 2"]
    }
  ],
  "metadata": {
    "verified": false,
    "created_at": "2026-01-26",
    "updated_at": "2026-01-26"
  }
}
```

### Quy tắc

- ✅ Thông tin chính xác
- ✅ Follow đúng format JSON
- ✅ Test local trước khi PR
- ✅ Một trường một PR

---

## 📂 Cấu trúc Data

Bạn có thể:
1. **Thêm vào file có sẵn:** `data/schools.json`
2. **Tạo file mới:** `data/hanoi-schools.json`, `data/hcm-schools.json`...

Script import tự động đọc **tất cả file `.json`** trong thư mục `data/`.

---

## 🚀 Deploy

### Production Server

```bash
# Clone repo
git clone https://github.com/ZenithHawking/schools-api.git
cd schools-api

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/import_data.py

# Tạo systemd service
sudo nano /etc/systemd/system/schools-api.service
```

**Service file:**
```ini
[Unit]
Description=Schools API
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
# Enable & start
sudo systemctl daemon-reload
sudo systemctl enable schools-api
sudo systemctl start schools-api
```

### Update Data

```bash
cd ~/schools-api
git pull origin main
source venv/bin/activate
python scripts/import_data.py
sudo systemctl restart schools-api
```

---

## 📊 Database Schema

| Table | Key Fields |
|-------|------------|
| **schools** | id, code, name, type, country |
| **faculties** | id, school_id, name, programs |
| **campuses** | id, school_id, name, address |

---

## 📝 License

MIT License - Free to use

---

## 📧 Contact

- **Issues:** [GitHub Issues](https://github.com/ZenithHawking/schools-api/issues)
- **API:** https://apihoavan.xyz/openapi/

Made with ❤️ by Zenith
