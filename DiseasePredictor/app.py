import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

# Set up the page
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# Load the saved models
# We use absolute paths to avoid errors
# Load the saved models
# We use simpler relative paths here
try:
    diabetes_model = pickle.load(open(get_resource_path('saved_models/diabetes_model.sav'), 'rb'))
    heart_model = pickle.load(open(get_resource_path('saved_models/heart_model.sav'), 'rb'))
except FileNotFoundError:
    st.error("Error: Model files not found. Make sure you are running this command from the 'DiseasePredictor' folder.")

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction',
        ['Diabetes Prediction', 'Heart Disease Prediction'],
        icons=['activity', 'heart'],
        default_index=0
    )

# --- Diabetes Page ---
if selected == 'Diabetes Prediction':
    st.title('🩸 Diabetes Prediction AI')
    st.write("Enter your details below to check diabetes risk.")

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', '0')
        SkinThickness = st.text_input('Skin Thickness value', '20')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', '0.5')
    with col2:
        Glucose = st.text_input('Glucose Level', '100')
        Insulin = st.text_input('Insulin Level', '30')
        Age = st.text_input('Age of the Person', '25')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value', '70')
        BMI = st.text_input('BMI value', '25')

    if st.button('Get Diabetes Result'):
        try:
            user_input = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
            prediction = diabetes_model.predict([3.3])

            if prediction[0] == 1:
                st.error('⚠️ Diagnosis: The person is likely Diabetic.')
            else:
                st.success('✅ Diagnosis: The person is NOT Diabetic.')
        except ValueError:
            st.warning("Please enter valid numbers only.")


# --- Heart Disease Page ---
if selected == 'Heart Disease Prediction':
    st.title('🫀 Heart Disease Prediction AI')
    st.write("Enter cardiac details to assess heart health.")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age', '50')
        trestbps = st.text_input('Resting Blood Pressure', '120')
        restecg = st.text_input('Resting ECG (0-2)', '0')
        oldpeak = st.text_input('ST depression', '1.0')
        thal = st.text_input('Thal (0-3)', '2')
    with col2:
        sex = st.text_input('Sex (1=Male, 0=Female)', '1')
        chol = st.text_input('Cholesterol', '200')
        thalach = st.text_input('Max Heart Rate', '150')
        slope = st.text_input('Slope (0-2)', '1')
    with col3:
        cp = st.text_input('Chest Pain Type (0-3)', '1')
        fbs = st.text_input('Fasting Blood Sugar > 120 (1=True, 0=False)', '0')
        exang = st.text_input('Exercise Induced Angina (1=Yes, 0=No)', '0')
        ca = st.text_input('Major Vessels (0-3)', '0')

    if st.button('Get Heart Result'):
        try:
            user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
            prediction = heart_model.predict([user_input])

            if prediction[0] == 1:
                st.error('⚠️ Diagnosis: The person likely has Heart Disease.')
            else:
                st.success('✅ Diagnosis: The person is Healthy.')
        except ValueError:

            st.warning("Please enter valid numbers only.")

