import datetime
import pandas as pd
import streamlit as st
import joblib
from sklearn.preprocessing import StandardScaler
import os

# Set a custom theme for the app
st.set_page_config(page_title="Jaya Jaya Institut Pendidikan Prediksi", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for better styling
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

# Function to load and cache the dataset
@st.cache_data
def load_data():
    if not os.path.exists('student_feature_corr.csv'):
        st.error("Dataset file 'student_feature_corr.csv' not found. Please ensure the file is in the correct directory.")
        st.stop()
    data = pd.read_csv('student_feature_corr.csv')
    data = data.drop(columns=['Status'], axis=1)
    return data

# Function for data preprocessing
def data_preprocessing(data_input, single_data, n, scaler):
    data = load_data()
    data = pd.concat([data_input, data])
    data = scaler.transform(data)
    if single_data:
        return data[[n]]
    else:
        return data[0:n]

# Function to load the model
def load_model():
    if not os.path.exists('model/model.joblib'):
        st.error("Model file 'model.joblib' not found. Please ensure the model is trained and saved in the 'model' directory.")
        st.stop()
    return joblib.load('model/model.joblib')

# Function to make predictions
def model_predict(data, model):
    return model.predict(data)

# Function to display prediction result
def display_prediction(output):
    if output == 1:
        st.balloons()
        st.success('🎉 **Graduate**', icon="✅")
        st.markdown("The model predicts this student is likely to **graduate**.")
    else:
        st.error('⚠️ **Dropout**', icon="❌")
        st.markdown("The model predicts this student is at risk of **dropping out**.")

def main():
    st.title('Jaya Jaya Institut Pendidikan Prediksi')

    # Mappings for categorical inputs
    gender_mapping = {'Male': 1, 'Female': 0}
    marital_status_mapping = {
        'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4, 'Facto Union': 5, 'Legally Seperated': 6
    }
    application_mapping = {
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

    # Input fields for single data
    with st.container():
        col_gender, col_age, col_marital = st.columns([2, 2, 3])
        with col_gender:
            gender = st.radio('Gender', options=['Male', 'Female'],
                              help='The gender of the student')
        with col_age:
            age = st.number_input('Age at Enrollment', min_value=17, max_value=70, step=1,
                                  help='The age of the student at the time of enrollment')
        with col_marital:
            marital_status = st.selectbox('Marital Status', ('Single', 'Married',
                                                            'Widower', 'Divorced', 'Facto Union', 'Legally Seperated'),
                                          help='The marital status of the student')

    st.write('')
    st.write('')

    with st.container():
        col_application, col_prev_grade, col_admission_grade = st.columns([3, 1.65, 1.1])
        with col_application:
            application_mode = st.selectbox('Application Mode', (
                '1st Phase - General Contingent',
                '1st Phase - Special Contingent (Azores Island)',
                '1st Phase - Special Contingent (Madeira Island)',
                '2nd Phase - General Contingent', '3rd Phase - General Contingent',
                'Ordinance No. 612/93', 'Ordinance No. 854-B/99',
                'Ordinance No. 533-A/99, Item B2 (Different Plan)',
                'Ordinance No. 533-A/99, Item B3 (Other Institution)',
                'International Student (Bachelor)', 'Over 23 Years Old',
                'Transfer', 'Change of Course', 'Holders of Other Higher Courses',
                'Short Cycle Diploma Holders',
                'Technological Specialization Diploma Holders',
                'Change of Institution/Course',
                'Change of Institution/Course (International)'),
                help='The method of application used by the student')
        with col_prev_grade:
            prev_qualification_grade = st.number_input('Previous Qualification Grade', min_value=0, max_value=200, step=1,
                                                      help='Grade of previous qualification (0-200)')
        with col_admission_grade:
            admission_grade = st.number_input('Admission Grade', min_value=0, max_value=200, step=1,
                                             help="Student's admission grade (0-200)")

    with st.container():
        col_scholarship, col_tuition, col_displaced, col_debtor = st.columns([1.7, 2.1, 1.55, 1])
        with col_scholarship:
            scholarship_holder = 1 if st.checkbox(
                'Scholarship', help='Whether the student is a scholarship holder') else 0
        with col_tuition:
            tuition_fees = 1 if st.checkbox(
                'Tuition up to date', help="Whether the student's tuition fees are up to date") else 0
        with col_displaced:
            displaced = 1 if st.checkbox(
                'Displaced', help='Whether the student is a displaced person') else 0
        with col_debtor:
            debtor = 1 if st.checkbox(
                'Debtor', help='Whether the student is a debtor') else 0

    st.write('')
    st.write('')

    with st.container():
        col_1_enroll, col_2_enroll, col_2_eval = st.columns([1, 1, 1.2])
        with col_1_enroll:
            curricular_units_1st_sem_enrolled = st.number_input(
                'Units 1st Semester Enrolled', min_value=0, max_value=26, step=1,
                help='The number of curricular units enrolled by the student in the first semester')
        with col_2_enroll:
            curricular_units_2nd_sem_enrolled = st.number_input(
                'Units 2nd Semester Enrolled', min_value=0, max_value=23, step=1,
                help='The number of curricular units enrolled by the student in the second semester')
        with col_2_eval:
            curricular_units_2nd_sem_evaluations = st.number_input(
                'Units 2nd Semester Evaluations', min_value=0, max_value=33, step=1,
                help='The number of curricular units evaluations by the student in the second semester')

    with st.container():
        col_1_approved, col_2_approved, col_2_noeval = st.columns([1, 1, 1.2])
        with col_1_approved:
            curricular_units_1st_sem_approved = st.number_input(
                'Units 1st Semester Approved', min_value=0, max_value=26, step=1,
                help='The number of curricular units approved by the student in the first semester')
        with col_2_approved:
            curricular_units_2nd_sem_approved = st.number_input(
                'Units 2nd Semester Approved', min_value=0, max_value=20, step=1,
                help='The number of curricular units approved by the student in the second semester')
        with col_2_noeval:
            curricular_units_2nd_sem_without_evaluations = st.number_input(
                'Units 2nd Semester No Evaluations', min_value=0, max_value=12, step=1,
                help='The number of curricular units without evaluations by the student in the second semester')

    with st.container():
        col_1_grade, col_2_grade, col_2_empty = st.columns([1, 1, 1.2])
        with col_1_grade:
            curricular_units_1st_sem_grade = st.number_input(
                'Units 1st Semester Grade', min_value=0, max_value=20, step=1,
                help='The number of curricular units grade by the student in the first semester')
        with col_2_grade:
            curricular_units_2nd_sem_grade = st.number_input(
                'Units 2nd Semester Grade', min_value=0, max_value=20, step=1,
                help='The number of curricular units grade by the student in the second semester')

    # Mapping the categorical data
    gender = gender_mapping.get(gender)
    marital_status = marital_status_mapping.get(marital_status)
    application_mode = application_mapping.get(application_mode)

    # Create DataFrame for input data
    data = [[marital_status, application_mode, prev_qualification_grade,
             admission_grade, displaced, debtor, tuition_fees,
             gender, scholarship_holder, age,
             curricular_units_1st_sem_enrolled,
             curricular_units_1st_sem_approved, curricular_units_1st_sem_grade,
             curricular_units_2nd_sem_enrolled,
             curricular_units_2nd_sem_evaluations,
             curricular_units_2nd_sem_approved, curricular_units_2nd_sem_grade,
             curricular_units_2nd_sem_without_evaluations]]

    data = pd.DataFrame(data, columns=[
        'Marital_status', 'Application_mode', 'Previous_qualification_grade',
        'Admission_grade', 'Displaced', 'Debtor', 'Tuition_fees_up_to_date',
        'Gender', 'Scholarship_holder', 'Age_at_enrollment',
        'Curricular_units_1st_sem_enrolled',
        'Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_grade',
        'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_2nd_sem_evaluations',
        'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
        'Curricular_units_2nd_sem_without_evaluations'])

    # Load the scaler and model
    scaler = StandardScaler().fit(load_data())
    model = load_model()

    # Predict button
    st.markdown("### Predict")
    if st.button(' Predict Student Status', use_container_width=True):
        data_input = data_preprocessing(data, True, 0, scaler)
        output = model_predict(data_input, model)
        display_prediction(output)

    st.write('')
    st.write('')

    year_now = datetime.date.today().year
    year = year_now if year_now == 2025 else f'2025 - {year_now}'
    name = "[Muhammad Reza Ubaidillah](https://www.linkedin.com/in/muhammadrezaubaidillah/ 'Muhammad Reza Ubaidillah | LinkedIn')"
    copyright = 'Copyright © ' + str(year) + ' ' + name
    st.caption(copyright)

if __name__ == '__main__':
    main()