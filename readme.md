## 🚀 Instalasi dan Cara Menjalankan

Ikuti langkah-langkah ini untuk menjalankan proyek secara lokal.

### Prasyarat

* Python 3.8+
* `pip` dan `venv`
* Browser web modern (Chrome, Firefox, dll.)

### Langkah-langkah

**1. Clone Repositori**
```bash
git clone [https://github.com/username/nama-repositori.git](https://github.com/username/nama-repositori.git)
cd nama-repositori
````

**2. Siapkan Model Machine Learning**

  * Masuk ke direktori model: `cd model`.
  * Buat *virtual environment*:
    ```bash
    python -m venv venv
    ```
  * Aktifkan *virtual environment*:
      * Windows: `venv\Scripts\activate`
      * macOS/Linux: `source venv/bin/activate`
  * Install semua *library* yang dibutuhkan:
    ```bash
    pip install -r requirements.txt
    ```
  * Unduh dataset gambar rontgen (misalnya dari Kaggle) dan letakkan di dalam folder `model/chest/` dengan struktur `train`, `val`, dan `test`.
  * Jalankan *notebook* `model.ipynb` untuk melatih model dan menghasilkan file `modelPneumonia.h5`.

**3. Siapkan Backend**

  * Salin file `modelPneumonia.h5` dari folder `/model` ke dalam folder `/backend/model/` (buat folder `model` jika belum ada).
  * Pindah ke direktori backend: `cd ../backend`.
  * (Opsional) Buat dan aktifkan *virtual environment* baru khusus untuk backend jika diinginkan.
  * Install semua *library* yang dibutuhkan:
    ```bash
    pip install -r requirements.txt
    ```

**4. Jalankan Backend Server**

  * Pastikan Anda berada di dalam direktori `/backend`.
  * Jalankan server Flask:
    ```bash
    python app.py
    ```
  * Server akan berjalan di `http://127.0.0.1:5000`.

**5. Jalankan Frontend**

  * Buka direktori `/frontend` di file explorer Anda.
  * Klik dua kali pada file `index.html` untuk membukanya di browser.

Aplikasi Anda sekarang siap digunakan\!

-----

## 📂 Struktur Proyek

```
.
├── backend/                # Kode server Flask
│   ├── model/
│   │   └── modelPneumonia.h5  # File model yang sudah dilatih
│   ├── uploads/            # Direktori sementara untuk gambar
│   ├── app.py              # Logika utama server
│   └── requirements.txt    # Kebutuhan library backend
│
├── frontend/               # Kode antarmuka pengguna
│   ├── index.html          # Halaman utama
│   ├── script.js           # Logika interaksi
│   └── style.css           # Styling tambahan
│
└── model/                  # Kode untuk melatih model
    ├── chest/              # (Direktori untuk dataset gambar)
    ├── model.ipynb         # Jupyter Notebook untuk training
    └── requirements.txt    # Kebutuhan library model
```

```

---