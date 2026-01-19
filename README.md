# 🎓 Vietnam Schools API

Community-driven open API for Vietnamese universities and colleges.

## 📖 Giới thiệu

API công khai cho phép truy cập thông tin về các trường đại học, cao đẳng tại Việt Nam. Dữ liệu được đóng góp và duy trì bởi cộng đồng.

## 🚀 Bắt đầu nhanh

### Cài đặt

```bash
# Clone repo
git clone https://github.com/yourusername/vietnam-schools-api.git
cd vietnam-schools-api

# Cài đặt dependencies
pip install -r requirements.txt

# Import dữ liệu mẫu
python scripts/import_data.py

# Chạy API
uvicorn app.main:app --reload
```

API sẽ chạy tại: `http://localhost:8000`

Docs tự động: `http://localhost:8000/docs`

## 📚 API Endpoints

### Schools

- `GET /api/v1/schools` - Danh sách trường
  - Query params: `skip`, `limit`, `country`, `type`, `verified`, `search`
- `GET /api/v1/schools/{school_id}` - Chi tiết trường
- `POST /api/v1/schools` - Tạo trường mới
- `PUT /api/v1/schools/{school_id}` - Cập nhật trường
- `DELETE /api/v1/schools/{school_id}` - Xóa trường

### Faculties

- `GET /api/v1/faculties` - Danh sách khoa
  - Query params: `skip`, `limit`, `school_id`, `search`
- `GET /api/v1/faculties/{faculty_id}` - Chi tiết khoa
- `GET /api/v1/schools/{school_id}/faculties` - Các khoa của trường

### Campuses

- `GET /api/v1/schools/{school_id}/campuses` - Các cơ sở của trường

## 📋 Ví dụ sử dụng

### Lấy danh sách trường

```bash
curl http://localhost:8000/api/v1/schools
```

### Tìm kiếm trường

```bash
curl "http://localhost:8000/api/v1/schools?search=bách%20khoa"
```

### Lọc theo loại trường

```bash
curl "http://localhost:8000/api/v1/schools?type=public&verified=true"
```

### Lấy thông tin chi tiết trường

```bash
curl http://localhost:8000/api/v1/schools/hcmus
```

### Lấy danh sách khoa của trường

```bash
curl http://localhost:8000/api/v1/schools/hcmus/faculties
```

## 🤝 Đóng góp dữ liệu

### Thêm trường mới

1. Fork repo này
2. Thêm thông tin trường vào `data/schools.json`
3. Tạo Pull Request

### Template trường mới

```json
{
  "id": "school_slug",
  "code": "XXX",
  "name": "Tên trường đầy đủ",
  "logo_url": null,
  "description": "Mô tả về trường",
  
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
      "address": "Địa chỉ đầy đủ",
      "is_main": true
    }
  ],
  
  "faculties": [
    {
      "id": "faculty_slug",
      "name": "Tên khoa",
      "code": "XX",
      "website": "https://...",
      "programs": ["Ngành 1", "Ngành 2"]
    }
  ],
  
  "metadata": {
    "verified": false,
    "created_at": "2025-01-19",
    "updated_at": "2025-01-19"
  }
}
```

## 🗂️ Cấu trúc dự án

```
vietnam-schools-api/
├── app/
│   ├── main.py          # FastAPI app + routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── database.py      # Database connection
├── data/
│   └── schools.json     # Dữ liệu nguồn
├── scripts/
│   └── import_data.py   # Script import JSON → DB
├── requirements.txt
└── README.md
```

## 📊 Schema Database

### School
- `id` (string) - Unique identifier
- `code` (string) - Mã trường
- `name` (string) - Tên trường
- `logo_url` (string, nullable)
- `description` (text)
- `type` (string) - public/private
- `country` (string) - Mã quốc gia
- `contact` (JSON) - Thông tin liên lạc
- `verified` (boolean)
- `created_at`, `updated_at`

### Campus
- `id` (int) - Auto increment
- `school_id` (string) - Foreign key
- `name` (string) - Tên cơ sở
- `address` (text) - Địa chỉ
- `is_main` (boolean)

### Faculty
- `id` (string) - Unique identifier
- `school_id` (string) - Foreign key
- `name` (string) - Tên khoa
- `code` (string) - Mã khoa
- `website` (string)
- `programs` (JSON) - Danh sách ngành

## 🛠️ Development

### Chạy với hot reload

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Re-import data

```bash
python scripts/import_data.py
```

## 📝 License

MIT License

## 🙏 Contributors

Cảm ơn tất cả những người đã đóng góp vào dự án!

---

Made with ❤️ by Vietnamese Developer Community
