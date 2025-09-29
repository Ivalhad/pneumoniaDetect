import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Inisialisasi aplikasi Flask
app = Flask(__name__)
CORS(app)

# Tentukan path ke model dan folder upload
MODEL_PATH = 'model/modelPneumonia.h5'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Muat model saat aplikasi pertama kali dijalankan
try:
    model = load_model(MODEL_PATH)
    print(f"* Model '{MODEL_PATH}' berhasil dimuat.")
except Exception as e:
    print(f"* Error memuat model: {e}")
    model = None

# --- BAGIAN BARU: Route untuk halaman utama ---
@app.route('/')
def home():
    """Endpoint untuk halaman utama."""
    return jsonify({
        'status': 'success',
        'message': 'Server deteksi pneumonia berjalan dengan baik!'
    })
# -------------------------------------------

def model_predict(img_path, model):
    """Fungsi untuk melakukan prediksi pada satu gambar."""
    img = image.load_img(img_path, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0
    preds = model.predict(x)
    return preds[0][0]

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model tidak dapat dimuat, cek log server.'}), 500
    
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dikirim'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nama file tidak boleh kosong'}), 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            prediction_value = model_predict(file_path, model)
            result = 'Pneumonia' if prediction_value > 0.5 else 'Normal'
            os.remove(file_path)
            
            return jsonify({
                'prediction': result,
                'confidence': float(prediction_value)
            })
        except Exception as e:
            # Jika terjadi error saat prediksi, akan ditangkap oleh error handler di bawah
            # Kita bisa memanggil error 500 secara eksplisit
            app.logger.error(f"Error saat prediksi: {e}")
            # Meneruskan error ke handler 500
            raise e
            
    return jsonify({'error': 'Terjadi kesalahan'}), 500

# --- BAGIAN BARU: Error handler untuk error server ---
@app.errorhandler(500)
def internal_server_error(e):
    """Handler untuk Internal Server Error."""
    return jsonify({
        'status': 'error',
        'message': 'Terjadi kesalahan internal pada server.',
        'details': str(e) # Menampilkan detail error
    }), 500
# ----------------------------------------------------

if __name__ == '__main__':
    app.run(port=5000, debug=True)