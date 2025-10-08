# test_db.py
import pymysql

try:
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='', # Tanpa password
        database='devnotex', # Nama database Anda
        port=3306
    )
    print("Koneksi berhasil! Database 'devnotex' ditemukan.")
    conn.close()
except pymysql.err.OperationalError as e:
    print(f"Koneksi GAGAL: {e}")