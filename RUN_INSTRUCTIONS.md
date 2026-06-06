# CompostMind - Cara Menjalankan Aplikasi

## Prasyarat
- Python 3.8 atau lebih tinggi
- Node.js (opsional, untuk development)
- Browser web modern (Chrome, Firefox, Edge)

## Langkah-langkah Menjalankan

### 1. Instal Dependencies Backend

Buka terminal/command prompt dan jalankan:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Jalankan Backend Server

Dari folder `backend`, jalankan:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server akan berjalan di `http://localhost:8000`

### 3. Buka Frontend

Ada beberapa cara untuk membuka frontend:

**Opsi A: Buka langsung file HTML**
- Buka file `Frontend/index.html` di browser Anda
- Atau drag & drop file tersebut ke browser

**Opsi B: Gunakan Live Server (direkomendasikan)**
Jika menggunakan VS Code:
1. Install ekstensi "Live Server"
2. Klik kanan pada `Frontend/index.html`
3. Pilih "Open with Live Server"

**Opsi C: Gunakan Python HTTP Server**
```bash
cd Frontend
python -m http.server 3000
```
Kemudian buka `http://localhost:3000` di browser

### 4. Mulai Analisis

**Mode Upload Gambar:**
1. Upload gambar sampah (banana atau paper) atau drag & drop
2. Sistem akan mengirim gambar ke backend untuk dianalisis menggunakan model YOLO (best.pt)
3. Hasil analisis akan ditampilkan dengan rekomendasi

**Mode Live Detection (Kamera):**
1. Klik "Take Photo" lalu "Start Camera"
2. Sistem akan otomatis mendeteksi objek secara live setiap 2 detik
3. Hasil deteksi akan ditampilkan real-time di panel "Live Detection"
4. Hanya objek **banana** dan **paper** yang dapat dideteksi
5. Jika objek lain terdeteksi, akan muncul pesan "Object not detected"
6. Klik tombol capture untuk mengambil foto dan melihat hasil detail

## Struktur API

### Endpoint: `/api/scan-kompos`

**Method:** POST  
**Content-Type:** multipart/form-data

**Request:**
- `file`: Gambar (JPG, JPEG, PNG)

**Response:**
```json
{
  "status": "success",
  "isCompostable": true,
  "itemName": "Banana",
  "confidence": 92.5,
  "detected_objects": ["banana"],
  "kesimpulan_logika": {
    "bisa_dikompos": true,
    "status": "Organik",
    "solusi": "Aman! Kulit pisang adalah materi organik yang bagus untuk kompos."
  }
}
```

**Catatan:** Model YOLO saat ini hanya dapat mendeteksi:
- `banana` (pisang) - Kompostable
- `paper` (kertas) - Kompostable dengan catatan

Jika objek lain terdeteksi, sistem akan mengembalikan status "Tidak Terdeteksi".

## Troubleshooting

### Backend tidak bisa dijalankan
- Pastikan semua dependencies sudah terinstall
- Pastikan file `best.pt` ada di folder `backend/`
- Periksa apakah port 8000 sudah digunakan aplikasi lain

### Frontend tidak bisa connect ke backend
- Pastikan backend sudah berjalan di `http://localhost:8000`
- Periksa console browser untuk error CORS (sudah dihandle di backend)
- Coba refresh halaman frontend

### Model YOLO gagal dimuat
- Pastikan file `best.pt` ada di folder yang sama dengan `app.py`
- Periksa apakah ultralytics sudah terinstall dengan benar

## Catatan Penting

- Frontend dan backend harus berjalan secara bersamaan
- Backend menggunakan CORS middleware untuk mengizinkan request dari frontend
- Jika backend mati, frontend akan menampilkan pesan error dan menggunakan fallback result