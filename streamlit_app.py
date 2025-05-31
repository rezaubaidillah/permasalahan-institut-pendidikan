import datetime
import pandas as pd
import streamlit as st
import joblib
from sklearn.preprocessing import StandardScaler
import os

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Jaya Jaya Institut Pendidikan, Prediksi Dropout", layout="wide", initial_sidebar_state="collapsed")

# CSS kustom untuk styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stNumberInput>label {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Fungsi untuk memuat dataset
@st.cache_data
def load_student_data():
    if not os.path.exists('student_feature_corr.csv'):
        st.error("File dataset 'student_feature_corr.csv' tidak ditemukan.")
        st.stop()
    data = pd.read_csv('student_feature_corr.csv')
    data = data.drop(columns=['Status'], axis=1)
    return data

# Fungsi untuk preprocessing data
def transform_input_data(input_data, scaler):
    return scaler.transform(input_data)

# Fungsi untuk memuat model
def get_prediction_model():
    if not os.path.exists('model/model.joblib'):
        st.error("File model 'model.joblib' tidak ditemukan.")
        st.stop()
    return joblib.load('model/model.joblib')

# Fungsi untuk membuat prediksi
def make_prediction(data, model):
    return model.predict(data)

# Fungsi untuk menampilkan hasil prediksi
def show_prediction_result(output):
    if output == 1:
        st.markdown("<h3 style='color: green;'>🎉 Lulus</h3>", unsafe_allow_html=True)
        st.markdown("Model memprediksi siswa ini kemungkinan akan **lulus**.")
    else:
        st.markdown("<h3 style='color: red;'>⚠️ Putus Sekolah</h3>", unsafe_allow_html=True)
        st.markdown("Model memprediksi siswa ini berisiko **putus sekolah**.")

def main():
    st.title('Jaya Jaya Institut Pendidikan Prediksi')

    # Pemetaan untuk input kategorikal
    gender_map = {'Male': 1, 'Female': 0}
    marital_map = {
        'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4, 'Facto Union': 5, 'Legally Seperated': 6
    }
    application_map = {
        '1st Phase - General Contingent': 1,
        '1st Phase - Special Contingent (Azores Island)': 5,
        '1st Phase - Special Contingent (Madeira Island)': 16,
        '2nd Phase - General Contingent': 17,
        '3rd Phase - General Contingent': 18,
        'Ordinance No. 612/93': 2,
        'Ordinance No. 854-B/99': 10,
        'Ordinance No. 533-A/99, Item B2 (Different Plan)': 26,
        'Ordinance No. 533-A/99, Item B3 (Other Institution)': 27,
        'International Student (Bachelor)': 15,
        'Over 23 Years Old': 39,
        'Transfer': 42,
        'Change of Course': 43,
        'Holders of Other Higher Courses': 7,
        'Short Cycle Diploma Holders': 53,
        'Technological Specialization Diploma Holders': 44,
        'Change of Institution/Course': 51,
        'Change of Institution/Course (International)': 57,
    }

    # Input pengguna
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 3])
        with col1:
            gender = st.radio('Jenis Kelamin', options=['Male', 'Female'], help='Jenis kelamin siswa')
        with col2:
            age = st.number_input('Usia saat Mendaftar', min_value=17, max_value=70, step=1, help='Usia siswa saat mendaftar')
        with col3:
            marital_status = st.selectbox('Status Perkawinan', ('Single', 'Married', 'Widower', 'Divorced', 'Facto Union', 'Legally Seperated'), help='Status perkawinan siswa')

    st.write('')
    with st.container():
        col4, col5, col6 = st.columns([3, 1.65, 1.1])
        with col4:
            application_mode = st.selectbox('Mode Aplikasi', list(application_map.keys()), help='Metode aplikasi siswa')
        with col5:
            prev_qualification_grade = st.number_input('Nilai Kualifikasi Sebelumnya', min_value=0, max_value=200, step=1, help='Nilai kualifikasi sebelumnya (0-200)')
        with col6:
            admission_grade = st.number_input('Nilai Penerimaan', min_value=0, max_value=200, step=1, help='Nilai penerimaan siswa (0-200)')

    st.write('')
    with st.container():
        col7, col8, col9, col10 = st.columns([1.7, 2.1, 1.55, 1])
        with col7:
            scholarship_holder = 1 if st.checkbox('Pemegang Beasiswa', help='Apakah siswa pemegang beasiswa') else 0
        with col8:
            tuition_fees = 1 if st.checkbox('Biaya Kuliah Terbaru', help='Apakah biaya kuliah siswa terbaru') else 0
        with col9:
            displaced = 1 if st.checkbox('Terdispersi', help='Apakah siswa terdispersi') else 0
        with col10:
            debtor = 1 if st.checkbox('Berutang', help='Apakah siswa berutang') else 0

    st.write('')
    with st.container():
        col11, col12, col13 = st.columns([1, 1, 1.2])
        with col11:
            curricular_units_1st_sem_enrolled = st.number_input('Unit Semester 1 Terdaftar', min_value=0, max_value=26, step=1, help='Jumlah unit terdaftar semester 1')
        with col12:
            curricular_units_2nd_sem_enrolled = st.number_input('Unit Semester 2 Terdaftar', min_value=0, max_value=23, step=1, help='Jumlah unit terdaftar semester 2')
        with col13:
            curricular_units_2nd_sem_evaluations = st.number_input('Evaluasi Semester 2', min_value=0, max_value=33, step=1, help='Jumlah evaluasi semester 2')

    st.write('')
    with st.container():
        col14, col15, col16 = st.columns([1, 1, 1.2])
        with col14:
            curricular_units_1st_sem_approved = st.number_input('Unit Semester 1 Disetujui', min_value=0, max_value=26, step=1, help='Jumlah unit disetujui semester 1')
        with col15:
            curricular_units_2nd_sem_approved = st.number_input('Unit Semester 2 Disetujui', min_value=0, max_value=20, step=1, help='Jumlah unit disetujui semester 2')
        with col16:
            curricular_units_2nd_sem_without_evaluations = st.number_input('Unit Semester 2 Tanpa Evaluasi', min_value=0, max_value=12, step=1, help='Jumlah unit tanpa evaluasi semester 2')

    st.write('')
    with st.container():
        col17, col18, col19 = st.columns([1, 1, 1.2])
        with col17:
            curricular_units_1st_sem_grade = st.number_input('Nilai Semester 1', min_value=0, max_value=20, step=1, help='Nilai unit semester 1')
        with col18:
            curricular_units_2nd_sem_grade = st.number_input('Nilai Semester 2', min_value=0, max_value=20, step=1, help='Nilai unit semester 2')

    # Memetakan data kategorikal
    gender = gender_map.get(gender)
    marital_status = marital_map.get(marital_status)
    application_mode = application_map.get(application_mode)

    # Membuat DataFrame untuk input
    input_data = pd.DataFrame([{
        'Marital_status': marital_status,
        'Application_mode': application_mode,
        'Previous_qualification_grade': prev_qualification_grade,
        'Admission_grade': admission_grade,
        'Displaced': displaced,
        'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition_fees,
        'Gender': gender,
        'Scholarship_holder': scholarship_holder,
        'Age_at_enrollment': age,
        'Curricular_units_1st_sem_enrolled': curricular_units_1st_sem_enrolled,
        'Curricular_units_1st_sem_approved': curricular_units_1st_sem_approved,
        'Curricular_units_1st_sem_grade': curricular_units_1st_sem_grade,
        'Curricular_units_2nd_sem_enrolled': curricular_units_2nd_sem_enrolled,
        'Curricular_units_2nd_sem_evaluations': curricular_units_2nd_sem_evaluations,
        'Curricular_units_2nd_sem_approved': curricular_units_2nd_sem_approved,
        'Curricular_units_2nd_sem_grade': curricular_units_2nd_sem_grade,
        'Curricular_units_2nd_sem_without_evaluations': curricular_units_2nd_sem_without_evaluations
    }])

    # Memuat dataset dan scaler
    dataset = load_student_data()
    scaler = StandardScaler().fit(dataset)

    # Memuat model
    model = get_prediction_model()

    # Tombol prediksi
    st.markdown("### Prediksi")
    if st.button('Prediksi Status Siswa', use_container_width=True):
        transformed_data = transform_input_data(input_data, scaler)
        prediction = make_prediction(transformed_data, model)
        show_prediction_result(prediction[0])

    st.write('')
    year_now = datetime.date.today().year
    year = year_now if year_now == 2025 else f'2025 - {year_now}'
    name = "[Muhammad Reza Ubaidillah](https://www.linkedin.com/in/muhammadrezaubaidillah/)"
    st.markdown(f"**Copyright © {year} {name}**", unsafe_allow_html=True)

if __name__ == '__main__':
    main()