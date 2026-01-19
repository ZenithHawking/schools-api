# 🎓 Schools and Universities API

> Community-driven open API for Vietnamese universities and colleges

🌐 **Live API:** https://apihoavan.xyz/openapi/

📖 **Documentation:** https://apihoavan.xyz/openapi/docs

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/ZenithHawking/schools-api)](https://github.com/ZenithHawking/schools-api/releases)

---

## 📖 Giới thiệu

API công khai miễn phí cung cấp thông tin về các trường đại học, cao đẳng tại Việt Nam và các quốc gia khác. Dữ liệu được đóng góp và duy trì bởi cộng đồng.

### ✨ Tính năng

- ✅ RESTful API với FastAPI
- ✅ Dữ liệu mở - Miễn phí sử dụng
- ✅ Hỗ trợ tìm kiếm & lọc dữ liệu
- ✅ Auto-generated documentation (Swagger UI)
- ✅ Community-driven - Ai cũng có thể đóng góp

---

## 🌐 Sử dụng API (Production)

### Base URL
```
https://apihoavan.xyz/openapi
```

### 📚 API Endpoints

#### Schools (Trường học)

```bash
# Lấy danh sách tất cả trường
GET https://apihoavan.xyz/openapi/api/v1/schools

# Lấy chi tiết một trường
GET https://apihoavan.xyz/openapi/api/v1/schools/{school_id}

# Tìm kiếm trường theo tên
GET https://apihoavan.xyz/openapi/api/v1/schools?search=bách+khoa

# Lọc theo loại trường (public/private)
GET https://apihoavan.xyz/openapi/api/v1/schools?type=public

# Lọc theo quốc gia
GET https://apihoavan.xyz/openapi/api/v1/schools?country=VN

# Lọc theo mã trường
GET https://apihoavan.xyz/openapi/api/v1/schools?code=QTD

# Lọc trường đã verify
GET https://apihoavan.xyz/openapi/api/v1/schools?verified=true

# Kết hợp nhiều filters
GET https://apihoavan.xyz/openapi/api/v1/schools?country=VN&type=public&verified=true
```

#### Faculties (Khoa)

```bash
# Lấy danh sách tất cả khoa
GET https://apihoavan.xyz/openapi/api/v1/faculties

# Lấy chi tiết một khoa
GET https://apihoavan.xyz/openapi/api/v1/faculties/{faculty_id}

# Lấy danh sách khoa của một trường
GET https://apihoavan.xyz/openapi/api/v1/schools/{school_id}/faculties

# Lọc khoa theo trường
GET https://apihoavan.xyz/openapi/api/v1/faculties?school_id=hcmus

# Tìm kiếm khoa
GET https://apihoavan.xyz/openapi/api/v1/faculties?search=toán
```

#### Campuses (Cơ sở)

```bash
# Lấy danh sách cơ sở của một trường
GET https://apihoavan.xyz/openapi/api/v1/schools/{school_id}/campuses
```

### 📋 Ví dụ Response

#### GET /api/v1/schools

```json
[
  {
    "id": "hcmus",
    "code": "QTD",
    "name": "Trường Đại học Khoa học Tự nhiên",
    "logo_url": null,
    "description": "Trường Đại học Khoa học Tự nhiên...",
    "type": "public",
    "country": "VN",
    "contact": {
      "website": "https://www.hcmus.edu.vn",
      "email": "dhkhtn@hcmus.edu.vn",
      "phone": "+84 28 38 351 096"
    },
    "campuses": [
      {
        "id": 1,
        "name": "Cơ sở 1",
        "address": "227 Nguyễn Văn Cừ, Quận 5, TP.HCM",
        "is_main": true,
        "school_id": "hcmus"
      }
    ],
    "faculties": [
      {
        "id": "hcmus_math_cs",
        "name": "Khoa Toán - Tin học",
        "code": "MTH",
        "website": "https://www.math.hcmus.edu.vn",
        "programs": ["Toán học", "Khoa học máy tính"],
        "school_id": "hcmus"
      }
    ],
    "verified": true,
    "created_at": "2025-01-19",
    "updated_at": "2025-01-19"
  }
]
```

### 🔗 Interactive Documentation

Truy cập Swagger UI để test API trực tiếp trên browser:

👉 **https://apihoavan.xyz/openapi/docs**

---

## 🚀 Deploy từ GitHub Release

### Yêu cầu

- Ubuntu 20.04+ hoặc Debian-based Linux
- Python 3.8+
- 100MB disk space
- Quyền sudo (để install systemd service)

### Bước 1: Tải Release

```bash
# Tải release mới nhất
wget https://github.com/ZenithHawking/schools-api/releases/latest/download/vietnam-schools-api-v1.0.3.tar.gz

# Hoặc tải version cụ thể
wget https://github.com/ZenithHawking/schools-api/releases/download/v1.0.3/vietnam-schools-api-v1.0.3.tar.gz
```

### Bước 2: Giải nén

```bash
tar -xzf vietnam-schools-api-v1.0.3.tar.gz
cd vietnam-schools-api
```

### Bước 3: Setup

```bash
# Chạy script setup tự động
bash setup.sh
```

Script này sẽ:
- ✅ Tạo Python virtual environment
- ✅ Cài đặt dependencies
- ✅ Import dữ liệu vào database
- ✅ Tạo file `schools.db`

### Bước 4: Install Service (Optional)

```bash
# Cài đặt như systemd service (chạy tự động khi khởi động)
sudo bash install-service.sh
```

Service sẽ:
- ✅ Auto-start khi server khởi động
- ✅ Auto-restart nếu bị crash
- ✅ Chạy ở background

### Bước 5: Kiểm tra

```bash
# Kiểm tra service status
sudo systemctl status vietnam-schools-api

# Xem logs
sudo journalctl -u vietnam-schools-api -f

# Test API
curl http://localhost:8000/api/v1/schools
```

### Cấu hình Nginx/Cloudflare Tunnel

Nếu muốn expose API ra internet, cấu hình reverse proxy:

**Nginx:**
```nginx
location /openapi/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

**Cloudflare Tunnel:**
```yaml
ingress:
  - hostname: yourdomain.com
    path: /openapi/*
    service: http://localhost:8000
```

### Update Version Mới

```bash
# Stop service
sudo systemctl stop vietnam-schools-api

# Backup version cũ
mv vietnam-schools-api vietnam-schools-api.backup

# Tải version mới
wget https://github.com/ZenithHawking/schools-api/releases/download/v1.0.4/vietnam-schools-api-v1.0.4.tar.gz
tar -xzf vietnam-schools-api-v1.0.4.tar.gz
cd vietnam-schools-api

# Setup & restart
bash setup.sh
sudo bash install-service.sh
```

---

## 💻 Development (Local)

### Clone Repository

```bash
git clone https://github.com/ZenithHawking/schools-api.git
cd schools-api
```

### Setup Environment

```bash
# Tạo virtual environment
python3 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Import Data

```bash
python scripts/import_data.py
```

### Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API sẽ chạy tại:
- API: http://localhost:8000/api/v1/schools
- Docs: http://localhost:8000/docs

---

## 🤝 Đóng góp dữ liệu

Chúng tôi hoan nghênh mọi đóng góp từ cộng đồng!

### Thêm trường mới

1. **Fork** repository này
2. **Edit** file `data/schools.json`
3. Thêm thông tin trường theo template bên dưới
4. **Commit** với message rõ ràng
5. Tạo **Pull Request**

### Template trường mới

```json
{
  "id": "school_slug",
  "code": "XXX",
  "name": "Tên trường đầy đủ",
  "logo_url": null,
  "description": "Mô tả về trường (2-3 câu)",
  
  "type": "public",
  "country": "VN",
  
  "contact": {
    "website": "https://...",
    "email": "contact@...",
    "phone": "+84 ..."
  },
  
  "campuses": [
    {
      "name": "Cơ sở 1",
      "address": "Số nhà, Đường, Quận/Huyện, Tỉnh/TP",
      "is_main": true
    }
  ],
  
  "faculties": [
    {
      "id": "faculty_slug",
      "name": "Tên khoa",
      "code": "XX",
      "website": "https://...",
      "programs": ["Ngành 1", "Ngành 2", "Ngành 3"]
    }
  ],
  
  "metadata": {
    "verified": false,
    "created_at": "2025-01-19",
    "updated_at": "2025-01-19"
  }
}
```

### Quy tắc đóng góp

- ✅ Thông tin chính xác, có nguồn
- ✅ Follow đúng format JSON
- ✅ Tên trường phải chính thức
- ✅ Website & email phải valid
- ✅ Test local trước khi PR

---

## 📊 Schema Database

### School Table
- `id` (string, PK) - Unique identifier (slug format)
- `code` (string, unique) - Mã trường (dùng trong tuyển sinh)
- `name` (string) - Tên trường đầy đủ
- `logo_url` (string, nullable) - URL logo trường
- `description` (text) - Mô tả về trường
- `type` (string) - Loại trường: public/private
- `country` (string) - Mã quốc gia (ISO 3166)
- `contact` (JSON) - {website, email, phone}
- `verified` (boolean) - Đã được verify chưa
- `created_at`, `updated_at` (string) - Timestamps

### Campus Table
- `id` (int, PK, auto-increment)
- `school_id` (string, FK → schools.id)
- `name` (string) - Tên cơ sở
- `address` (text) - Địa chỉ đầy đủ
- `is_main` (boolean) - Cơ sở chính hay không

### Faculty Table
- `id` (string, PK) - Unique identifier
- `school_id` (string, FK → schools.id)
- `name` (string) - Tên khoa
- `code` (string) - Mã khoa
- `website` (string) - Website khoa
- `programs` (JSON) - ["Ngành 1", "Ngành 2", ...]

---

## 🗂️ Cấu trúc Project

```
schools-api/
├── .github/
│   └── workflows/
│       └── release.yml       # GitHub Actions workflow
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + routes
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── database.py          # Database connection
├── data/
│   └── schools.json         # Dữ liệu nguồn (JSON)
├── scripts/
│   └── import_data.py       # Script import JSON → SQLite
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

- **Backend:** FastAPI 0.109.0
- **Database:** SQLite (development), PostgreSQL (production recommended)
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic 2.5
- **Server:** Uvicorn
- **CI/CD:** GitHub Actions

---

## 📝 License

MIT License

---

## 🙏 Contributors

Cảm ơn tất cả những người đã đóng góp vào dự án!

[Contributor list](https://github.com/ZenithHawking/schools-api/graphs/contributors)

---

## 📧 Contact

- **Issues:** https://github.com/ZenithHawking/schools-api/issues
- **Discussions:** https://github.com/ZenithHawking/schools-api/discussions
- **API Status:** https://apihoavan.xyz/openapi/

---

Made by Zenith/Thanh Hải
