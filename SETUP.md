# DevNoteX - Setup Guide

Complete setup guide untuk DevNoteX platform (React + FastAPI + MySQL).

## Prerequisites

1. **Python 3.9+**
2. **Node.js 18+**
3. **MySQL 8.0+**
4. **npm** atau **yarn**

## Database Setup

### 1. Install MySQL

Download dan install MySQL dari [mysql.com](https://dev.mysql.com/downloads/mysql/)

### 2. Buat Database

Login ke MySQL dan jalankan:

```sql
CREATE DATABASE devnotex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. (Opsional) Buat User Khusus

```sql
CREATE USER 'devnotex'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON devnotex.* TO 'devnotex'@'localhost';
FLUSH PRIVILEGES;
```

## Backend Setup (FastAPI)

### 1. Navigate ke Backend Directory

```bash
cd backend
```

### 2. Buat Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variables

Buat file `.env` di direktori `backend/`:

```env
DATABASE_URL=mysql+pymysql://root:your_mysql_password@localhost:3306/devnotex
SECRET_KEY=change-this-to-random-secure-key-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**PENTING:**
- Ganti `your_mysql_password` dengan password MySQL Anda
- Untuk production, generate `SECRET_KEY` yang secure menggunakan:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### 5. Jalankan Backend

```bash
python main.py
```

Backend akan berjalan di **http://localhost:8000**

- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

### 6. Verifikasi Database

Saat backend pertama kali dijalankan, aplikasi akan:
1. Membuat semua tabel secara otomatis
2. Menyediakan seed data (demo user dan project)

**Demo Account:**
- Email: `demo@devnotex.com`
- Password: `testpass`

## Frontend Setup (React + Vite)

### 1. Install Dependencies

Dari root directory project:

```bash
npm install
```

### 2. Konfigurasi Environment

File `.env` sudah tersedia dengan konfigurasi default:

```env
VITE_API_URL=http://localhost:8000
```

Tidak perlu diubah untuk development lokal.

### 3. Jalankan Development Server

```bash
npm run dev
```

Frontend akan berjalan di **http://localhost:5173**

## Testing the Application

### 1. Akses Frontend

Buka browser dan navigate ke: http://localhost:5173

### 2. Login

Gunakan demo account:
- Email: `demo@devnotex.com`
- Password: `testpass`

Atau buat akun baru melalui halaman Register.

### 3. Test Features

- Create project baru
- Add notes, tasks, dan documents
- Test API endpoints via Swagger UI (http://localhost:8000/docs)

## Production Deployment

### Backend Production Setup

1. **Install Gunicorn** (production WSGI server):
```bash
pip install gunicorn
```

2. **Update Environment Variables:**
```env
DATABASE_URL=mysql+pymysql://user:password@production-host:3306/devnotex
SECRET_KEY=<secure-random-key>
```

3. **Run with Gunicorn:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Frontend Production Build

1. **Build aplikasi:**
```bash
npm run build
```

2. **Deploy folder `dist/`** ke web server (Nginx, Apache) atau hosting platform (Vercel, Netlify)

3. **Update `.env` production:**
```env
VITE_API_URL=https://your-api-domain.com
```

## Troubleshooting

### Backend tidak start

**Error: "Can't connect to MySQL server"**
- Pastikan MySQL service running
- Cek kredensial di `.env`
- Test koneksi: `mysql -u root -p`

**Error: "No module named X"**
- Pastikan virtual environment aktif
- Jalankan ulang: `pip install -r requirements.txt`

### Frontend tidak bisa connect ke API

**CORS Error**
- Pastikan backend running
- Cek konfigurasi CORS di `backend/main.py`
- Pastikan `allow_origins` include `http://localhost:5173`

**401 Unauthorized**
- Token expired (default 30 menit)
- Login ulang

### Database Issues

**Table doesn't exist**
- Hapus database: `DROP DATABASE devnotex;`
- Buat ulang: `CREATE DATABASE devnotex;`
- Restart backend (tables akan auto-created)

## Architecture Overview

```
DevNoteX/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Entry point
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── routers/               # API endpoints
│   ├── utils/                 # Auth, database utilities
│   └── requirements.txt       # Python dependencies
│
├── src/                        # React Frontend
│   ├── pages/                 # Page components
│   ├── components/            # UI components
│   ├── hooks/                 # Custom React hooks
│   └── utils/                 # API client (Axios)
│
└── package.json               # Node dependencies
```

## API Documentation

Setelah backend running, akses dokumentasi lengkap di:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Security Notes

1. **NEVER** commit `.env` files ke Git
2. Gunakan strong `SECRET_KEY` di production
3. Gunakan HTTPS di production
4. Secure MySQL dengan firewall rules
5. Regular database backups

## Support

Untuk pertanyaan lebih lanjut, check:
- API Docs: http://localhost:8000/docs
- Database schema: Lihat file `backend/models/`
- Frontend routes: Lihat `src/App.tsx`
