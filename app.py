import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_option_menu import option_menu
import pickle
from PIL import Image
import numpy as np
import plotly.figure_factory as ff
import streamlit as st
from code.DiseaseModel import DiseaseModel
from code.helper import prepare_symptoms_array
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os

# PWA Configuration - Makes app installable on mobile
st.set_page_config(
    page_title="Disease Prediction App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/disease-prediction',
        'Report a bug': 'https://github.com/yourusername/disease-prediction/issues',
        'About': '# Multiple Disease Prediction App\nAI-powered disease prediction system'
    }
)

# Add PWA meta tags and manifest
st.markdown("""
    <head>
        <!-- PWA Configuration -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Disease Predict">
        <meta name="application-name" content="Disease Prediction">
        <meta name="theme-color" content="#FF4B4B">
        
        <!-- App Icons -->
        <link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192x192.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/assets/logo.png">
        <link rel="manifest" href="/manifest.json">
        
        <!-- Splash Screen -->
        <meta name="msapplication-TileColor" content="#0E1117">
        <meta name="msapplication-TileImage" content="/assets/icon-512x512.png">
    </head>
""", unsafe_allow_html=True)

# loading the models
diabetes_model = joblib.load("models/diabetes_model.sav")
heart_model = joblib.load("models/heart_disease_model.sav")
parkinson_model = joblib.load("models/parkinsons_model.sav")
# Load the lung cancer prediction model
lung_cancer_model = joblib.load('models/lung_cancer_model.sav')

# Load the hepatitis prediction model
hepatitis_model = joblib.load('models/hepititisc_model.sav')


liver_model = joblib.load('models/liver_model.sav')# Load the lung cancer prediction model
lung_cancer_model = joblib.load('models/lung_cancer_model.sav')


# sidebar
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction', [
        'Disease Prediction',
        'Diabetes Prediction',
        'Heart disease Prediction',
        'Parkison Prediction',
        'Liver prediction',
        'Hepatitis prediction',
        'Lung Cancer Prediction',
        'Skin Disease Prediction',

    ],
        icons=['','activity', 'heart', 'person','person','person','person','bandaid'],
        default_index=0)




# multiple disease prediction
if selected == 'Disease Prediction': 
    # Create disease class and load ML model
    disease_model = DiseaseModel()
    disease_model.load_xgboost('model/xgboost_model.json')

    # Title
    st.write('# Disease Prediction using Machine Learning')

    symptoms = st.multiselect('What are your symptoms?', options=disease_model.all_symptoms)

    X = prepare_symptoms_array(symptoms)

    # Trigger XGBoost model
    if st.button('Predict'): 
        # Run the model with the python script
        
        prediction, prob = disease_model.predict(X)
        st.write(f'## Disease: {prediction} with {prob*100:.2f}% probability')


        tab1, tab2= st.tabs(["Description", "Precautions"])

        with tab1:
            st.write(disease_model.describe_predicted_disease())

        with tab2:
            precautions = disease_model.predicted_disease_precautions()
            for i in range(4):
                st.write(f'{i+1}. {precautions[i]}')




# Diabetes prediction page
if selected == 'Diabetes Prediction':  # pagetitle
    st.title("Diabetes disease prediction")
    image = Image.open('d3.jpg')
    st.image(image, caption='diabetes disease prediction')
    # columns
    # no inputs from the user
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input("Number of Pregnencies")
    with col2:
        Glucose = st.number_input("Glucose level")
    with col3:
        BloodPressure = st.number_input("Blood pressure  value")
    with col1:

        SkinThickness = st.number_input("Sckinthickness value")

    with col2:

        Insulin = st.number_input("Insulin value ")
    with col3:
        BMI = st.number_input("BMI value")
    with col1:
        DiabetesPedigreefunction = st.number_input(
            "Diabetespedigreefunction value")
    with col2:

        Age = st.number_input("AGE")

    # code for prediction
    diabetes_dig = ''

    # button
    if st.button("Diabetes test result"):
        diabetes_prediction=[[]]
        diabetes_prediction = diabetes_model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreefunction, Age]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if diabetes_prediction[0] == 1:
            diabetes_dig = "we are really sorry to say but it seems like you are Diabetic."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            diabetes_dig = 'Congratulation,You are not diabetic'
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name+' , ' + diabetes_dig)
        
        



# Heart prediction page
if selected == 'Heart disease Prediction':
    st.title("Heart disease prediction")
    image = Image.open('heart2.jpg')
    st.image(image, caption='heart failuire')
    # age	sex	cp	trestbps	chol	fbs	restecg	thalach	exang	oldpeak	slope	ca	thal	target
    # columns
    # no inputs from the user
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age")
    with col2:
        sex=0
        display = ("male", "female")
        options = list(range(len(display)))
        value = st.selectbox("Gender", options, format_func=lambda x: display[x])
        if value == "male":
            sex = 1
        elif value == "female":
            sex = 0
    with col3:
        cp=0
        display = ("typical angina","atypical angina","non — anginal pain","asymptotic")
        options = list(range(len(display)))
        value = st.selectbox("Chest_Pain Type", options, format_func=lambda x: display[x])
        if value == "typical angina":
            cp = 0
        elif value == "atypical angina":
            cp = 1
        elif value == "non — anginal pain":
            cp = 2
        elif value == "asymptotic":
            cp = 3
    with col1:
        trestbps = st.number_input("Resting Blood Pressure")

    with col2:

        chol = st.number_input("Serum Cholestrol")
    
    with col3:
        restecg=0
        display = ("normal","having ST-T wave abnormality","left ventricular hyperthrophy")
        options = list(range(len(display)))
        value = st.selectbox("Resting ECG", options, format_func=lambda x: display[x])
        if value == "normal":
            restecg = 0
        elif value == "having ST-T wave abnormality":
            restecg = 1
        elif value == "left ventricular hyperthrophy":
            restecg = 2

    with col1:
        exang=0
        thalach = st.number_input("Max Heart Rate Achieved")
   
    with col2:
        oldpeak = st.number_input("ST depression induced by exercise relative to rest")
    with col3:
        slope=0
        display = ("upsloping","flat","downsloping")
        options = list(range(len(display)))
        value = st.selectbox("Peak exercise ST segment", options, format_func=lambda x: display[x])
        if value == "upsloping":
            slope = 0
        elif value == "flat":
            slope = 1
        elif value == "downsloping":
            slope = 2
    with col1:
        ca = st.number_input("Number of major vessels (0–3) colored by flourosopy")
    with col2:
        thal=0
        display = ("normal","fixed defect","reversible defect")
        options = list(range(len(display)))
        value = st.selectbox("thalassemia", options, format_func=lambda x: display[x])
        if value == "normal":
            thal = 0
        elif value == "fixed defect":
            thal = 1
        elif value == "reversible defect":
            thal = 2
    with col3:
        agree = st.checkbox('Exercise induced angina')
        if agree:
            exang = 1
        else:
            exang=0
    with col1:
        agree1 = st.checkbox('fasting blood sugar > 120mg/dl')
        if agree1:
            fbs = 1
        else:
            fbs=0
    # code for prediction
    heart_dig = ''
    

    # button
    if st.button("Heart test result"):
        heart_prediction=[[]]
        # change the parameters according to the model
        
        # b=np.array(a, dtype=float)
        heart_prediction = heart_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        if heart_prediction[0] == 1:
            heart_dig = 'we are really sorry to say but it seems like you have Heart Disease.'
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            
        else:
            heart_dig = "Congratulation , You don't have Heart Disease."
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name +' , ' + heart_dig)









if selected == 'Parkison Prediction':
    st.title("Parkison prediction")
    image = Image.open('p1.jpg')
    st.image(image, caption='parkinsons disease')
  # parameters
#    name	MDVP:Fo(Hz)	MDVP:Fhi(Hz)	MDVP:Flo(Hz)	MDVP:Jitter(%)	MDVP:Jitter(Abs)	MDVP:RAP	MDVP:PPQ	Jitter:DDP	MDVP:Shimmer	MDVP:Shimmer(dB)	Shimmer:APQ3	Shimmer:APQ5	MDVP:APQ	Shimmer:DDA	NHR	HNR	status	RPDE	DFA	spread1	spread2	D2	PPE
   # change the variables according to the dataset used in the model
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)
    with col1:
        MDVP = st.number_input("MDVP:Fo(Hz)")
    with col2:
        MDVPFIZ = st.number_input("MDVP:Fhi(Hz)")
    with col3:
        MDVPFLO = st.number_input("MDVP:Flo(Hz)")
    with col1:
        MDVPJITTER = st.number_input("MDVP:Jitter(%)")
    with col2:
        MDVPJitterAbs = st.number_input("MDVP:Jitter(Abs)")
    with col3:
        MDVPRAP = st.number_input("MDVP:RAP")

    with col2:

        MDVPPPQ = st.number_input("MDVP:PPQ ")
    with col3:
        JitterDDP = st.number_input("Jitter:DDP")
    with col1:
        MDVPShimmer = st.number_input("MDVP:Shimmer")
    with col2:
        MDVPShimmer_dB = st.number_input("MDVP:Shimmer(dB)")
    with col3:
        Shimmer_APQ3 = st.number_input("Shimmer:APQ3")
    with col1:
        ShimmerAPQ5 = st.number_input("Shimmer:APQ5")
    with col2:
        MDVP_APQ = st.number_input("MDVP:APQ")
    with col3:
        ShimmerDDA = st.number_input("Shimmer:DDA")
    with col1:
        NHR = st.number_input("NHR")
    with col2:
        HNR = st.number_input("HNR")
  
    with col2:
        RPDE = st.number_input("RPDE")
    with col3:
        DFA = st.number_input("DFA")
    with col1:
        spread1 = st.number_input("spread1")
    with col1:
        spread2 = st.number_input("spread2")
    with col3:
        D2 = st.number_input("D2")
    with col1:
        PPE = st.number_input("PPE")

    # code for prediction
    parkinson_dig = ''
    
    # button
    if st.button("Parkinson test result"):
        parkinson_prediction=[[]]
        # change the parameters according to the model
        parkinson_prediction = parkinson_model.predict([[MDVP, MDVPFIZ, MDVPFLO, MDVPJITTER, MDVPJitterAbs, MDVPRAP, MDVPPPQ, JitterDDP, MDVPShimmer,MDVPShimmer_dB, Shimmer_APQ3, ShimmerAPQ5, MDVP_APQ, ShimmerDDA, NHR, HNR,  RPDE, DFA, spread1, spread2, D2, PPE]])

        if parkinson_prediction[0] == 1:
            parkinson_dig = 'we are really sorry to say but it seems like you have Parkinson disease'
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            parkinson_dig = "Congratulation , You don't have Parkinson disease"
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name+' , ' + parkinson_dig)



# Load the dataset
lung_cancer_data = pd.read_csv('data/lung_cancer.csv')

# Convert 'M' to 0 and 'F' to 1 in the 'GENDER' column
lung_cancer_data['GENDER'] = lung_cancer_data['GENDER'].map({'M': 'Male', 'F': 'Female'})

# Lung Cancer prediction page
if selected == 'Lung Cancer Prediction':
    st.title("Lung Cancer Prediction")
    image = Image.open('h.png')
    st.image(image, caption='Lung Cancer Prediction')

    # Columns
    # No inputs from the user
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender:", lung_cancer_data['GENDER'].unique())
    with col2:
        age = st.number_input("Age")
    with col3:
        smoking = st.selectbox("Smoking:", ['NO', 'YES'])
    with col1:
        yellow_fingers = st.selectbox("Yellow Fingers:", ['NO', 'YES'])

    with col2:
        anxiety = st.selectbox("Anxiety:", ['NO', 'YES'])
    with col3:
        peer_pressure = st.selectbox("Peer Pressure:", ['NO', 'YES'])
    with col1:
        chronic_disease = st.selectbox("Chronic Disease:", ['NO', 'YES'])

    with col2:
        fatigue = st.selectbox("Fatigue:", ['NO', 'YES'])
    with col3:
        allergy = st.selectbox("Allergy:", ['NO', 'YES'])
    with col1:
        wheezing = st.selectbox("Wheezing:", ['NO', 'YES'])

    with col2:
        alcohol_consuming = st.selectbox("Alcohol Consuming:", ['NO', 'YES'])
    with col3:
        coughing = st.selectbox("Coughing:", ['NO', 'YES'])
    with col1:
        shortness_of_breath = st.selectbox("Shortness of Breath:", ['NO', 'YES'])

    with col2:
        swallowing_difficulty = st.selectbox("Swallowing Difficulty:", ['NO', 'YES'])
    with col3:
        chest_pain = st.selectbox("Chest Pain:", ['NO', 'YES'])

    # Code for prediction
    cancer_result = ''

    # Button
    if st.button("Predict Lung Cancer"):
        # Create a DataFrame with user inputs
        user_data = pd.DataFrame({
            'GENDER': [gender],
            'AGE': [age],
            'SMOKING': [smoking],
            'YELLOW_FINGERS': [yellow_fingers],
            'ANXIETY': [anxiety],
            'PEER_PRESSURE': [peer_pressure],
            'CHRONICDISEASE': [chronic_disease],
            'FATIGUE': [fatigue],
            'ALLERGY': [allergy],
            'WHEEZING': [wheezing],
            'ALCOHOLCONSUMING': [alcohol_consuming],
            'COUGHING': [coughing],
            'SHORTNESSOFBREATH': [shortness_of_breath],
            'SWALLOWINGDIFFICULTY': [swallowing_difficulty],
            'CHESTPAIN': [chest_pain]
        })

        # Map string values to numeric
        user_data.replace({'NO': 1, 'YES': 2}, inplace=True)

        # Strip leading and trailing whitespaces from column names
        user_data.columns = user_data.columns.str.strip()

        # Convert columns to numeric where necessary
        numeric_columns = ['AGE', 'FATIGUE', 'ALLERGY', 'ALCOHOLCONSUMING', 'COUGHING', 'SHORTNESSOFBREATH']
        user_data[numeric_columns] = user_data[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Perform prediction
        cancer_prediction = lung_cancer_model.predict(user_data)

        # Display result
        if cancer_prediction[0] == 'YES':
            cancer_result = "The model predicts that there is a risk of Lung Cancer."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            cancer_result = "The model predicts no significant risk of Lung Cancer."
            image = Image.open('negative.jpg')
            st.image(image, caption='')

        st.success(name + ', ' + cancer_result)




# Liver prediction page
if selected == 'Liver prediction':  # pagetitle
    st.title("Liver disease prediction")
    image = Image.open('liver.jpg')
    st.image(image, caption='Liver disease prediction.')
    # columns
    # no inputs from the user
# st.write(info.astype(int).info())
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        Sex=0
        display = ("male", "female")
        options = list(range(len(display)))
        value = st.selectbox("Gender", options, format_func=lambda x: display[x])
        if value == "male":
            Sex = 0
        elif value == "female":
            Sex = 1
    with col2:
        age = st.number_input("Entre your age") # 2 
    with col3:
        Total_Bilirubin = st.number_input("Entre your Total_Bilirubin") # 3
    with col1:
        Direct_Bilirubin = st.number_input("Entre your Direct_Bilirubin")# 4

    with col2:
        Alkaline_Phosphotase = st.number_input("Entre your Alkaline_Phosphotase") # 5
    with col3:
        Alamine_Aminotransferase = st.number_input("Entre your Alamine_Aminotransferase") # 6
    with col1:
        Aspartate_Aminotransferase = st.number_input("Entre your Aspartate_Aminotransferase") # 7
    with col2:
        Total_Protiens = st.number_input("Entre your Total_Protiens")# 8
    with col3:
        Albumin = st.number_input("Entre your Albumin") # 9
    with col1:
        Albumin_and_Globulin_Ratio = st.number_input("Entre your Albumin_and_Globulin_Ratio") # 10 
    # code for prediction
    liver_dig = ''

    # button
    if st.button("Liver test result"):
        liver_prediction=[[]]
        liver_prediction = liver_model.predict([[Sex,age,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if liver_prediction[0] == 1:
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            liver_dig = "we are really sorry to say but it seems like you have liver disease."
        else:
            image = Image.open('negative.jpg')
            st.image(image, caption='')
            liver_dig = "Congratulation , You don't have liver disease."
        st.success(name+' , ' + liver_dig)






# Hepatitis prediction page
if selected == 'Hepatitis prediction':
    st.title("Hepatitis Prediction")
    image = Image.open('h.png')
    st.image(image, caption='Hepatitis Prediction')

    # Columns
    # No inputs from the user
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Enter your age")  # 2
    with col2:
        sex = st.selectbox("Gender", ["Male", "Female"])
        sex = 1 if sex == "Male" else 2
    with col3:
        total_bilirubin = st.number_input("Enter your Total Bilirubin")  # 3

    with col1:
        direct_bilirubin = st.number_input("Enter your Direct Bilirubin")  # 4
    with col2:
        alkaline_phosphatase = st.number_input("Enter your Alkaline Phosphatase")  # 5
    with col3:
        alamine_aminotransferase = st.number_input("Enter your Alamine Aminotransferase")  # 6

    with col1:
        aspartate_aminotransferase = st.number_input("Enter your Aspartate Aminotransferase")  # 7
    with col2:
        total_proteins = st.number_input("Enter your Total Proteins")  # 8
    with col3:
        albumin = st.number_input("Enter your Albumin")  # 9

    with col1:
        albumin_and_globulin_ratio = st.number_input("Enter your Albumin and Globulin Ratio")  # 10

    with col2:
        your_ggt_value = st.number_input("Enter your GGT value")  # Add this line
    with col3:
        your_prot_value = st.number_input("Enter your PROT value")  # Add this line

    # Code for prediction
    hepatitis_result = ''

    # Button
    if st.button("Predict Hepatitis"):
        # Create a DataFrame with user inputs
        user_data = pd.DataFrame({
            'Age': [age],
            'Sex': [sex],
            'ALB': [total_bilirubin],  # Correct the feature name
            'ALP': [direct_bilirubin],  # Correct the feature name
            'ALT': [alkaline_phosphatase],  # Correct the feature name
            'AST': [alamine_aminotransferase],
            'BIL': [aspartate_aminotransferase],  # Correct the feature name
            'CHE': [total_proteins],  # Correct the feature name
            'CHOL': [albumin],  # Correct the feature name
            'CREA': [albumin_and_globulin_ratio],  # Correct the feature name
            'GGT': [your_ggt_value],  # Replace 'your_ggt_value' with the actual value
            'PROT': [your_prot_value]  # Replace 'your_prot_value' with the actual value
        })

        # Perform prediction
        hepatitis_prediction = hepatitis_model.predict(user_data)
        # Display result
        if hepatitis_prediction[0] == 1:
            hepatitis_result = "We are really sorry to say but it seems like you have Hepatitis."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            hepatitis_result = 'Congratulations, you do not have Hepatitis.'
            image = Image.open('negative.jpg')
            st.image(image, caption='')

        st.success(name + ', ' + hepatitis_result)











# jaundice prediction page
if selected == 'Jaundice prediction':  # pagetitle
    st.title("Jaundice disease prediction")
    image = Image.open('j.jpg')
    st.image(image, caption='Jaundice disease prediction')
    # columns
    # no inputs from the user
# st.write(info.astype(int).info())
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Entre your age   ") # 2 
    with col2:
        Sex=0
        display = ("male", "female")
        options = list(range(len(display)))
        value = st.selectbox("Gender", options, format_func=lambda x: display[x])
        if value == "male":
            Sex = 0
        elif value == "female":
            Sex = 1
    with col3:
        Total_Bilirubin = st.number_input("Entre your Total_Bilirubin") # 3
    with col1:
        Direct_Bilirubin = st.number_input("Entre your Direct_Bilirubin")# 4

    with col2:
        Alkaline_Phosphotase = st.number_input("Entre your Alkaline_Phosphotase") # 5
    with col3:
        Alamine_Aminotransferase = st.number_input("Entre your Alamine_Aminotransferase") # 6
    with col1:
        Total_Protiens = st.number_input("Entre your Total_Protiens")# 8
    with col2:
        Albumin = st.number_input("Entre your Albumin") # 9 
    # code for prediction
    jaundice_dig = ''

    # button
    if st.button("Jaundice test result"):
        jaundice_prediction=[[]]
        jaundice_prediction = liver_model.predict([[age,Sex,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Total_Protiens,Albumin]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if jaundice_prediction[0] == 1:
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            jaundice_dig = "we are really sorry to say but it seems like you have Jaundice."
        else:
            image = Image.open('negative.jpg')
            st.image(image, caption='')
            jaundice_dig = "Congratulation , You don't have Jaundice."
        st.success(name+' , ' + jaundice_dig)












from sklearn.preprocessing import LabelEncoder
import joblib


# Skin Disease Prediction Page
if selected == 'Skin Disease Prediction':
    import requests
    import base64
    from io import BytesIO
    import time
    
    # Custom CSS for dark theme and styling
    st.markdown("""
    <style>
        .main-title {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: #FF6B6B;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 18px;
            text-align: center;
            color: #95A5A6;
            margin-bottom: 30px;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        .result-card {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .disease-name {
            font-size: 32px;
            font-weight: bold;
            color: #FF6B6B;
            text-align: center;
            margin: 15px 0;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .confidence-badge {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        }
        .info-section {
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        .info-title {
            font-size: 22px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        .info-item {
            color: #ECF0F1;
            font-size: 16px;
            line-height: 1.8;
            padding: 5px 0;
        }
        .warning-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        }
        .disclaimer {
            background: rgba(255,107,107,0.1);
            border: 2px solid #FF6B6B;
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
            text-align: center;
        }
        .disclaimer-title {
            font-size: 24px;
            font-weight: bold;
            color: #FF6B6B;
            margin-bottom: 10px;
        }
        .disclaimer-text {
            font-size: 16px;
            color: #ECF0F1;
            line-height: 1.6;
        }
        .upload-box {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            background: rgba(102, 126, 234, 0.1);
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<p class="main-title">🔬 AI Skin Disease Detection</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload an image for instant AI-powered analysis</p>', unsafe_allow_html=True)
    
    # Logo/Icon
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.markdown("""
        <div style="text-align: center; font-size: 80px; margin: 20px 0;">
            🩺
        </div>
        """, unsafe_allow_html=True)
    
    # Information about the system
    with st.expander("ℹ️ About This AI System", expanded=False):
        st.markdown("""
        ### How It Works
        This advanced AI system uses **Deep Learning (Convolutional Neural Networks)** to analyze skin images 
        and detect various skin conditions.
        
        ### Detectable Conditions:
        - 🔴 **Acne** - Inflammatory skin condition
        - 🟠 **Eczema** - Atopic dermatitis
        - 🟡 **Psoriasis** - Autoimmune skin disorder
        - 🟢 **Ringworm** - Fungal infection
        - 🔵 **Melanoma** - Skin cancer (requires urgent medical attention)
        - ⚪ **Healthy Skin** - No apparent condition
        
        ### Instructions:
        1. Upload a clear, well-lit image (JPG or PNG)
        2. Click "Analyze Image"
        3. View your results with detailed information
        4. Consult a dermatologist for professional diagnosis
        """)
    
    # File uploader
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📸 Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the affected skin area"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display uploaded image
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 📷 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True, caption="Image for Analysis")
        
        # Predict button
        if st.button("🔍 Analyze Image", key="predict_skin"):
            with st.spinner('🤖 Deep Learning AI is analyzing your image... This may take 10-30 seconds...'):
                try:
                    # API endpoint
                    API_URL = "http://localhost:5001/predict"
                    
                    # Reset file pointer
                    uploaded_file.seek(0)
                    
                    # Prepare file for upload
                    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    # Make API request with extended timeout
                    try:
                        response = requests.post(API_URL, files=files, timeout=60)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if result.get('success'):
                                # Success animation
                                st.balloons()
                                
                                prediction = result.get('prediction', {})
                                details = result.get('details', {})
                                
                                # Results container
                                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                                
                                # Disease name
                                disease_name = prediction.get('disease', 'Unknown')
                                st.markdown(f'<p class="disease-name">🎯 {disease_name}</p>', unsafe_allow_html=True)
                                
                                # Confidence
                                confidence = prediction.get('confidence', 0)
                                st.markdown(
                                    f'<div style="text-align: center;"><span class="confidence-badge">Confidence: {confidence:.1f}%</span></div>',
                                    unsafe_allow_html=True
                                )
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Warning for Melanoma
                                if 'melanoma' in disease_name.lower():
                                    st.markdown("""
                                    <div class="warning-box">
                                        ⚠️ URGENT WARNING ⚠️<br>
                                        Melanoma is a serious form of skin cancer.<br>
                                        Please consult an oncologist or dermatologist IMMEDIATELY!
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Display all probabilities
                                with st.expander("📊 All Disease Probabilities", expanded=False):
                                    all_probs = prediction.get('all_probabilities', {})
                                    for disease, prob in sorted(all_probs.items(), key=lambda x: x[1], reverse=True):
                                        st.progress(prob / 100)
                                        st.write(f"**{disease}**: {prob:.2f}%")
                                
                                # Detailed Information Tabs
                                tab1, tab2, tab3, tab4 = st.tabs([
                                    "🩺 Symptoms",
                                    "🔬 Causes",
                                    "🛡️ Precautions",
                                    "💊 Treatments"
                                ])
                                
                                with tab1:
                                    st.markdown('<div class="info-section">', unsafe_allow_html=True)
                                    st.markdown('<p class="info-title">Common Symptoms</p>', unsafe_allow_html=True)
                                    symptoms = details.get('symptoms', [])
                                    for symptom in symptoms:
                                        st.markdown(f'<p class="info-item">• {symptom}</p>', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                with tab2:
                                    st.markdown('<div class="info-section">', unsafe_allow_html=True)
                                    st.markdown('<p class="info-title">Possible Causes</p>', unsafe_allow_html=True)
                                    causes = details.get('causes', [])
                                    for cause in causes:
                                        st.markdown(f'<p class="info-item">• {cause}</p>', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                with tab3:
                                    st.markdown('<div class="info-section">', unsafe_allow_html=True)
                                    st.markdown('<p class="info-title">Recommended Precautions</p>', unsafe_allow_html=True)
                                    precautions = details.get('precautions', [])
                                    for precaution in precautions:
                                        st.markdown(f'<p class="info-item">• {precaution}</p>', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                with tab4:
                                    st.markdown('<div class="info-section">', unsafe_allow_html=True)
                                    st.markdown('<p class="info-title">Treatment Options</p>', unsafe_allow_html=True)
                                    treatments = details.get('treatments', [])
                                    for treatment in treatments:
                                        st.markdown(f'<p class="info-item">• {treatment}</p>', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Special warning if present
                                if details.get('warning'):
                                    st.markdown(f"""
                                    <div class="warning-box">
                                        {details.get('warning')}
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Medical Disclaimer
                                st.markdown("""
                                <div class="disclaimer">
                                    <p class="disclaimer-title">⚕️ Medical Disclaimer</p>
                                    <p class="disclaimer-text">
                                        This is an AI-based screening tool and NOT a confirmed medical diagnosis.
                                        The predictions are for informational purposes only. Please consult a 
                                        qualified dermatologist or healthcare professional for proper diagnosis 
                                        and treatment. Do not use this tool as a substitute for professional 
                                        medical advice.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            else:
                                st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
                                st.info(result.get('message', ''))
                        
                        else:
                            st.error(f"❌ API Error (Status {response.status_code})")
                            error_data = response.json()
                            st.error(error_data.get('error', 'Unknown error'))
                            st.info(error_data.get('message', 'Please try again'))
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to AI server")
                        st.warning("""
                        **The AI backend is not running.**
                        
                        To start the AI server:
                        1. Open a new terminal
                        2. Navigate to: `skin_disease_api/`
                        3. Run: `python app.py`
                        4. Wait for server to start
                        5. Try uploading again
                        """)
                    
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timeout - Analysis took longer than 60 seconds. Please try again with a smaller image or wait for the server to warm up.")
                        st.info("💡 Tip: The first prediction after starting the server takes longer. Subsequent predictions will be faster!")
                    
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Error processing image: {str(e)}")
    
    else:
        # Show sample information when no image is uploaded
        st.info("👆 Please upload an image to get started")
        
        # Show statistics or features
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 40px;">🎯</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">6</div>
                <div style="color: #95A5A6;">Disease Classes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 40px;">🤖</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">AI</div>
                <div style="color: #95A5A6;">Deep Learning</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 40px;">⚡</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">Fast</div>
                <div style="color: #95A5A6;">Instant Results</div>
            </div>
            """, unsafe_allow_html=True)

