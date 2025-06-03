# Import library yang diperlukan
from flask import Flask, render_template, request, flash  # Flask untuk membuat web app
import cv2  # OpenCV untuk pengolahan gambar
import os  # Untuk operasi file dan direktori
from werkzeug.utils import secure_filename  # Untuk keamanan nama file
from edge_detection import detect_edges  # Import fungsi deteksi tepi

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Diperlukan untuk flash messages

# Pengaturan folder untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'static/upload'
# Tipe file yang diizinkan untuk diunggah
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Konfigurasi folder upload ke aplikasi Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Membuat folder upload jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Memeriksa apakah file yang diunggah memiliki ekstensi yang diizinkan
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Fungsi utama untuk menangani upload file dan proses deteksi tepi
    """
    if request.method == 'POST':
        try:
            # Memeriksa apakah ada file yang diunggah
            if 'file' not in request.files:
                flash('Tidak ada file yang dipilih', 'error')
                return render_template('index.html')
            
            file = request.files['file']
            # Memeriksa apakah user memilih file
            if file.filename == '':
                flash('Tidak ada file yang dipilih', 'error')
                return render_template('index.html')
            
            # Memproses file jika tipe filenya diizinkan
            if file and allowed_file(file.filename):
                # Membuat nama file yang aman
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Menyimpan file yang diunggah
                file.save(filepath)
                
                # Proses deteksi tepi menggunakan fungsi dari edge_detection.py
                output_filename = 'processed_' + filename
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                
                # Memastikan file berhasil disimpan
                if not os.path.exists(filepath):
                    flash('Gagal menyimpan file', 'error')
                    return render_template('index.html')
                
                # Proses deteksi tepi
                detect_edges(filepath, output_path)
                
                # Memastikan hasil deteksi tepi berhasil disimpan
                if not os.path.exists(output_path):
                    flash('Gagal memproses gambar', 'error')
                    return render_template('index.html')
                
                # Menampilkan hasil di halaman web
                return render_template('index.html', 
                                    original=filename, 
                                    processed=output_filename)
            else:
                flash('Tipe file tidak diizinkan. Gunakan PNG, JPG, atau JPEG', 'error')
                return render_template('index.html')
                
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return render_template('index.html')
    
    # Menampilkan halaman upload jika method GET
    return render_template('index.html')

# Menjalankan aplikasi jika file dijalankan langsung
if __name__ == '__main__':
    app.run(debug=True)  # Mode debug aktif untuk development

