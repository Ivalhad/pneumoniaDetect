import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Inisialisasi aplikasi Flask
app = Flask(__name__)
CORS(app)  # Mengizinkan Cross-Origin Resource Sharing

# Tentukan path ke model dan folder upload
MODEL_PATH = 'model/modelPneumonia.h5'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder uploads ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Muat model saat aplikasi pertama kali dijalankan (efisiensi)
try:
    model = load_model(MODEL_PATH)
    print(f"* Model '{MODEL_PATH}' berhasil dimuat.")
except Exception as e:
    print(f"* Error memuat model: {e}")
    model = None

def model_predict(img_path, model):
    """
    Fungsi untuk melakukan prediksi pada satu gambar.
    """
    # Memuat dan memproses gambar
    img = image.load_img(img_path, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # Normalisasi

    # Melakukan prediksi
    preds = model.predict(x)
    return preds[0][0]

# Definisikan API endpoint untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model tidak dapat dimuat, cek log server.'}), 500

    # Cek apakah ada file yang diunggah
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dikirim'}), 400
    
    file = request.files['file']

    # Cek apakah nama file kosong
    if file.filename == '':
        return jsonify({'error': 'Nama file tidak boleh kosong'}), 400

    if file:
        # Simpan file sementara di folder uploads
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Lakukan prediksi
        try:
            prediction_value = model_predict(file_path, model)

            # Interpretasi hasil prediksi
            if prediction_value > 0.5:
                result = 'Pneumonia'
            else:
                result = 'Normal'
            
            # Hapus file setelah prediksi (opsional, untuk menjaga kebersihan)
            os.remove(file_path)

            # Kirim hasil dalam format JSON
            return jsonify({
                'prediction': result,
                'confidence': float(prediction_value)
            })
        except Exception as e:
            return jsonify({'error': f'Gagal melakukan prediksi: {e}'}), 500
            
    return jsonify({'error': 'Terjadi kesalahan'}), 500

# Jalankan server
if __name__ == '__main__':
    # Gunakan port 5000 dan jalankan dalam mode debug
    app.run(port=5000, debug=True)