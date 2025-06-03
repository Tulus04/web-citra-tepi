# Import library yang diperlukan
import cv2  # OpenCV untuk pengolahan gambar
import os  # Untuk operasi file dan direktori

def detect_edges(image_path, output_path):
    """
    Fungsi untuk mendeteksi tepi pada gambar
    
    Parameter:
    - image_path: Lokasi file gambar yang akan diproses
    - output_path: Lokasi untuk menyimpan hasil deteksi tepi
    
    Proses:
    1. Membaca gambar dari file
    2. Mengubah gambar ke skala abu-abu
    3. Mengurangi noise dengan Gaussian Blur
    4. Mendeteksi tepi menggunakan algoritma Canny
    5. Menyimpan hasil deteksi tepi
    """
    try:
        # Membaca gambar dari file
        img = cv2.imread(image_path)
        if img is None:
            raise Exception("Gagal membaca gambar")

        # Mengubah gambar ke skala abu-abu untuk memudahkan deteksi tepi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Mengurangi noise pada gambar dengan Gaussian Blur
        # Kernel size (5,5) dan sigma 0 adalah parameter standar
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Mendeteksi tepi menggunakan algoritma Canny
        # threshold1=50 dan threshold2=150 adalah nilai ambang batas untuk deteksi tepi
        edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

        # Menyimpan hasil deteksi tepi ke file
        cv2.imwrite(output_path, edges)
        return output_path
    except Exception as e:
        print(f"Error dalam proses deteksi tepi: {str(e)}")
        raise