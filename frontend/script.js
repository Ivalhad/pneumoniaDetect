//elemen HTML ke JavaScript
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const resultArea = document.getElementById('result-area');
const imagePreview = document.getElementById('image-preview');
const loader = document.getElementById('loader');
const resultText = document.getElementById('result-text');
const predictionLabel = document.getElementById('prediction-label');
const confidenceLabel = document.getElementById('confidence-label');
const resetButton = document.getElementById('reset-button');

// URL API Backend Flask
const API_ENDPOINT = 'http://127.0.0.1:5000/predict';

// --- event listeners ---

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// menambahkan highlight saat gambar diseret ke area upload
['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => uploadArea.classList.add('bg-blue-50', 'border-blue-500'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('bg-blue-50', 'border-blue-500'), false);
});

// fungsi file yang di drop
uploadArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// fungsi file yang di pilih
fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});


function handleFiles(files) {
    if (files.length === 0) {
        console.log('Tidak ada file yang dipilih.');
        return;
    }
    const file = files[0];
    
    previewImage(file);
    
    uploadAndPredict(file);
}

function previewImage(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // tampilan dari area upload ke area hasil
    uploadArea.classList.add('hidden');
    resultArea.classList.remove('hidden');
    loader.classList.remove('hidden');
    resultText.classList.add('hidden');
}

async function uploadAndPredict(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Error dari server: ${response.statusText}`);
        }

        const data = await response.json();
        displayResult(data);

    } catch (error) {
        console.error('Gagal melakukan prediksi:', error);
        displayError(error.message);
    }
}

function displayResult(data) {
    loader.classList.add('hidden');
    resultText.classList.remove('hidden');

    const prediction = data.prediction;
    const confidence = (data.confidence * 100).toFixed(2);

    predictionLabel.textContent = prediction;
    confidenceLabel.textContent = `Tingkat Akurasi: ${confidence}%`;

    if (prediction === 'Pneumonia') {
        predictionLabel.className = 'text-4xl font-bold text-red-600';
    } else {
        predictionLabel.className = 'text-4xl font-bold text-green-600';
    }
}

function displayError(errorMessage) {
    loader.classList.add('hidden');
    resultText.classList.remove('hidden');
    predictionLabel.textContent = 'Error';
    predictionLabel.className = 'text-4xl font-bold text-yellow-500';
    confidenceLabel.textContent = `Detail: ${errorMessage}`;
}


// --- reset ---

resetButton.addEventListener('click', () => {
    uploadArea.classList.remove('hidden');
    resultArea.classList.add('hidden');
    fileInput.value = '';
});