# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan tinggi yang berdiri sejak tahun 2000. Hingga saat ini, institusi ini telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun, tingginya jumlah siswa yang tidak menyelesaikan pendidikan (dropout) menjadi masalah besar bagi institusi ini. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang berpotensi dropout agar dapat memberikan bimbingan khusus untuk mengurangi tingkat dropout dan meningkatkan tingkat kelulusan.

### Permasalahan Bisnis
Permasalahan bisnis yang akan diselesaikan dalam proyek ini adalah:
- Mengidentifikasi faktor-faktor utama yang memengaruhi tingginya tingkat dropout di Jaya Jaya Institut.

### Cakupan Proyek
Cakupan proyek yang akan dikerjakan meliputi:
- Melakukan analisis data untuk memahami pola dan tren yang berkaitan dengan dropout.
- Membangun model machine learning untuk menentukan fitur-fitur penting yang dapat membantu mencegah dropout dan memprediksi apakah seorang mahasiswa akan dropout atau tidak.

### Persiapan

**Sumber Data:**  
Data yang digunakan berasal dari [https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md).

**Setup Environment:**  
1. Clone repository berikut:  
   [https://github.com/rezaubaidillah/Menyelesaikan-Permasalahan-Human-Resources.git](https://github.com/rezaubaidillah/Menyelesaikan-Permasalahan-Human-Resources.git)  
2. Jalankan file `notebook.ipynb`:  
   - Pastikan dependensi, packages, dan library yang dibutuhkan sudah tersedia (lihat file `requirements.txt` untuk daftar dependensi).  
   - Jalankan seluruh isi file `notebook.ipynb` menggunakan Google Colab atau Jupyter Notebook untuk melihat hasil analisis data, temuan, dan insight yang diperoleh.  
3. Menjalankan dashboard:  
   - Pull image Metabase:  
     ```
     docker pull metabase/metabase:v0.46.4
     ```  
   - Jalankan container Metabase:  
     ```
     docker run -p 3000:3000 --name metabase metabase/metabase
     ```  
   - Login ke Metabase dengan kredensial:  
     - Username: `root@mail.com`  
     - Password: `root123`

## Business Dashboard
Business dashboard yang telah dibuat menyajikan visualisasi data mahasiswa Jaya Jaya Institut untuk mendukung analisis tingkat dropout dan strategi retensi. Dashboard ini mencakup:  
- **Komposisi Mahasiswa**: Total 4,424 mahasiswa, dengan 110 mahasiswa internasional (2,5%) dan 4,314 mahasiswa lokal (97,5%).  
- **Distribusi Status Mahasiswa**: 49,9% lulus (Graduate), 32,1% dropout, dan 17,9% masih terdaftar (Enrolled), menyoroti tingkat dropout yang signifikan.  
- **Performa Akademik**: Grafik batang menampilkan hubungan antara jumlah unit kurikuler semester kedua yang disetujui (0-20) dengan status mahasiswa (Dropout, Enrolled, Graduate). Mahasiswa dengan lebih banyak unit yang disetujui cenderung lulus, sementara yang lebih sedikit berisiko dropout.  
- **Komposisi Gender**: 64,8% perempuan dan 35,2% laki-laki, memberikan gambaran demografi mahasiswa.  
- **Beasiswa**: Menyajikan data terkait beasiswa (total 4,424 mahasiswa),
Dashboard ini membantu mengidentifikasi pola risiko dropout berdasarkan performa akademik dan demografi, mendukung pengambilan keputusan untuk intervensi dini seperti bimbingan akademik atau perluasan beasiswa.


## Menjalankan Sistem Machine Learning
Prototype sistem machine learning yang telah dibuat dapat dijalankan dengan langkah berikut:  
- Jalankan aplikasi Streamlit menggunakan perintah:  
  ```
  streamlit run streamlit_app.py
  ```
  - atau gunakan link berikut : [https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md](https://permasalahan-institut-pendidikan.streamlit.app/).
  ```
  streamlit run streamlit_app.py
  ```  
Sistem ini memungkinkan prediksi apakah seorang siswa berisiko dropout berdasarkan fitur-fitur yang telah diidentifikasi.

## Conclusion
Berdasarkan analisis data dan pengembangan model machine learning, ditemukan bahwa beberapa fitur memiliki pengaruh signifikan terhadap kemungkinan siswa untuk dropout. Berikut adalah 10 fitur teratas berdasarkan koefisien model:  
1. **Curricular_units_2nd_sem_approved**: Semakin banyak unit kurikuler yang disetujui pada semester kedua, semakin rendah kemungkinan dropout.  
2. **Curricular_units_2nd_sem_enrolled**: Semakin banyak unit kurikuler yang diambil pada semester kedua, semakin tinggi kemungkinan dropout.  
3. **Curricular_units_1st_sem_approved**: Semakin banyak unit kurikuler yang disetujui pada semester pertama, semakin rendah kemungkinan dropout.  
4. **Tuition_fees_up_to_date**: Siswa yang membayar biaya kuliah tepat waktu memiliki kemungkinan dropout lebih rendah.  
5. **Curricular_units_1st_sem_enrolled**: Semakin banyak unit kurikuler yang diambil pada semester pertama, semakin tinggi kemungkinan dropout.  
6. **Curricular_units_2nd_sem_grade**: Nilai rata-rata semester kedua yang lebih tinggi mengurangi kemungkinan dropout.  
7. **Scholarship_holder**: Siswa penerima beasiswa memiliki kemungkinan dropout lebih rendah.  
8. **Debtor**: Siswa yang memiliki hutang cenderung lebih mungkin dropout.  
9. **Marital_status**: Status pernikahan memengaruhi kemungkinan dropout.  
10. **Curricular_units_1st_sem_grade**: Nilai rata-rata semester pertama yang lebih rendah meningkatkan kemungkinan dropout.  

Model machine learning yang dibangun mampu memprediksi siswa yang berisiko dropout dengan akurasi yang baik berdasarkan fitur-fitur tersebut.

### Rekomendasi Action Items
Berikut adalah rekomendasi tindakan yang dapat dilakukan Jaya Jaya Institut untuk mengurangi tingkat dropout:  
- **Meningkatkan Dukungan Akademik:**  
  - Menyediakan bimbingan akademik tambahan bagi siswa yang mengambil banyak unit kurikuler.  
  - Mendorong siswa untuk mengambil beban kurikuler yang sesuai dengan kemampuan mereka.  
- **Mengelola Keuangan Siswa:**  
  - Memperkuat program beasiswa dan bantuan keuangan.  
  - Menyediakan layanan konseling keuangan untuk mengelola hutang dan biaya kuliah.  
- **Meningkatkan Kinerja Akademik:**  
  - Menyediakan program remedial atau tutoring bagi siswa dengan nilai rendah.  
  - Memberikan insentif untuk mempertahankan nilai rata-rata yang baik.  
- **Menyediakan Dukungan Sosial:**  
  - Menyediakan layanan konseling untuk siswa dengan kesulitan pribadi, termasuk yang sudah menikah.  
  - Membangun komunitas siswa yang saling mendukung.  
- **Monitoring dan Intervensi Dini:**  
  - Menggunakan model machine learning untuk mengidentifikasi siswa berisiko secara dini.  
  - Memberikan intervensi khusus seperti bimbingan akademik atau konseling.  
- **Meningkatkan Komunikasi:**  
  - Meningkatkan komunikasi antara siswa, dosen, dan staf untuk memastikan siswa merasa didukung.
