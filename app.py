import streamlit as st
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
#loaded_model = joblib.load("model.joblib")

st.markdown(
    '<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.1/css/mdb.min.css" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
st.markdown("""""", unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
    
                header{visibility:hidden;}
                .main {
                    margin-top: -20px;
                    padding-top:10px;
                }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}

            </style>
            
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #405cE2;">
    <a class="navbar-brand" href="#"  target="_blank">Breast Cancer Predictor</a>  
    </nav>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>",unsafe_allow_html=True)
with st.form(key="form"):
    col1,col2, col3 = st.columns(3)
    with col1:
        with st.expander("#1"):
            Age = st.selectbox("please input age",['Young','Older','Middle-aged'])
            if Age=="Young":
                Age =0
            elif Age=="Middle-aged":
                Age =1
            elif Age=="Older":
                Age=2
            Gender = st.selectbox("Gender",['Male','Female'])
            if Gender=="Male":
                Gender =0
            elif Gender=="Female":
                Gender =1
           
            Pregnancy_Age = st.selectbox("please input Pregnancy age",['Young','Older','Middle-aged'])
            if Pregnancy_Age=="Young":
                Pregnancy_Age =0
            elif Pregnancy_Age=="Middle-aged":
                Pregnancy_Age =1
            elif Pregnancy_Age=="Older":
                Pregnancy_Age=2
            Bmi = st.selectbox("please input BMI",['Young','Older','Middle-aged'])
            if Bmi=="Young":
                Bmi =0
            elif Bmi=="Middle-aged":
                Bmi =1
            elif Bmi=="Older":
                Bmi=2
            Alcohol_Consumption = st.selectbox("please select Alcohol Consumption Level",['None','Low','High','Moderate'])
            if Alcohol_Consumption=="None":
                Alcohol_Consumption =0
            elif Alcohol_Consumption=="Low":
                Alcohol_Consumption =1
            elif Alcohol_Consumption=="High":
                Alcohol_Consumption=3
            elif Alcohol_Consumption=="Moderate":
                Alcohol_Consumption=2
    with col2:
        with st.expander("#2"):
            Inherited_Gene = st.selectbox("Inherited Gene",['Absent','Present'])
            if Inherited_Gene=="Absent":
                Inherited_Gene =0
            elif Inherited_Gene=="Present":
                Inherited_Gene =1
            Family_History = st.selectbox("Family History",['Present','Absent'])
            if Family_History=="Absent":
                Family_History =0
            elif Family_History=="Present":
                Family_History =1
            Radiation_Exposure = st.selectbox("Radiation Exposure",['Low','Moderate','High','None'])
            if Radiation_Exposure=="None":
                Radiation_Exposure =0
            elif Radiation_Exposure=="Low":
                Radiation_Exposure =1
            elif Radiation_Exposure=="High":
                Radiation_Exposure=3
            elif Radiation_Exposure=="Moderate":
                Radiation_Exposure=2
            Birth_Control = st.selectbox("Birth Control",['None','Low','High','Moderate'])
            if Birth_Control=="None":
                Birth_Control =0
            elif Birth_Control=="Low":
                Birth_Control =1
            elif Birth_Control=="High":
                Birth_Control=3
            elif Birth_Control=="Moderate":
                Birth_Control=2
            Hormone_Therapy = st.selectbox("please selectHormone Therapy",['None','Low','High','Moderate'])
            if Hormone_Therapy=="None":
                Hormone_Therapy =0
            elif Hormone_Therapy=="Low":
                Hormone_Therapy =1
            elif Hormone_Therapy=="High":
                Hormone_Therapy=3
            elif Hormone_Therapy=="Moderate":
                Hormone_Therapy=2
    with col3:
        with st.expander("#3"):
            Previous_History = st.selectbox("Previous History",['Absent','Present'])
            if Previous_History=="Absent":
                Previous_History =0
            elif Previous_History=="Present":
                Previous_History =1
            Desnse_Breast = st.selectbox("Densed Breast",['Absent','Present'])
            if Desnse_Breast=="Absent":
                Desnse_Breast =0
            elif Desnse_Breast=="Present":
                Desnse_Breast =1
            Menstrual_Cycle_Age =st.selectbox("please input Menstrual Cycle",['Young','Older','Middle-aged'])
            if Menstrual_Cycle_Age=="Young":
                Menstrual_Cycle_Age =0
            elif Menstrual_Cycle_Age=="Middle-age":
                Menstrual_Cycle_Age =1
            elif Menstrual_Cycle_Age=="Older":
                Menstrual_Cycle_Age=2
            Last_Menstrual_Cycle_Age = st.selectbox("please input last Menstrual Cycle",['Young','Older','Middle-aged'])
            if Last_Menstrual_Cycle_Age=="Young":
                Last_Menstrual_Cycle_Age =0
            elif Last_Menstrual_Cycle_Age=="Middle-aged":
                Last_Menstrual_Cycle_Age =1
            elif Last_Menstrual_Cycle_Age=="Older":
                Last_Menstrual_Cycle_Age=2
            Hormonal = st.selectbox("Homonal Imbalanced/Balanced",['Imbalanced','Balanced'])
            if Hormonal=="Imbalanced":
                Hormonal =0
            elif Hormonal=="Balanced":
                Hormonal =1
    button = st.form_submit_button("click")
# if not (age,gender,bmi,age_at_first_menstrual_cycle,family_history,birth_control_drugs,age_at_first_pregnancy,age_at_last_menstrual_cycle,postmenopausal_hormone_therapy,alcohol_intake,inherited_gene_mutation,previous_history,hormonal,dense_breast_tissue,obesity):
#     st.markdown(f"<h2 style='margin-left:-130px; ' class=' btn alert alert-danger'>input is required</h2>",unsafe_allow_html=True)


data = pd.read_csv(r"main.csv")

# Replace string values with digits using a dictionary
data.replace({
    "Gender": {"Female": 0, "Male": 1},
    "Family History": {"Absent": 0, "Present": 1},
    "BMI": {"None": 0, "Low": 1, "Moderate": 2, "High": 3},
    "Radiation Exposure": {"Low": 0, "Moderate": 1, "High": 2},
    "Birth Control": {"None": 0, "Low": 1, "Moderate": 2, "High": 3},
    "Hormone Therapy": {"None": 0, "Low": 1, "Moderate": 2, "High": 3},
    "Alcohol Consumption": {"None": 0, "Low": 1, "Moderate": 2, "High": 3},
    "Inherited Gene": {"Absent": 0, "Present": 1},
    "Previous History": {"None": 0, "Present": 1},
    "Menstrual Cycle Age": {"Young": 0, "Middle-aged": 1, "Older": 2},
    "Last Menstrual Cycle Age": {"Young": 0, "Middle-aged": 1, "Older": 2},
    "Pregnancy Age": {"Young": 0, "Middle-aged": 1, "Older": 2},
    "Hormonal": {"Balanced": 0, "Imbalanced": 1},
    "Dense Breast Tissue": {"Absent": 0, "Present": 1},
    "Risk": {"Low": 0, "Moderate": 1, "High": 2}
}, inplace=True)
data = data.dropna()
# Split the data into training and testing sets
X = data.drop(["Risk","Age"], axis=1)
y = data["Risk"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)
# Sample input values for prediction
sample_input = {
    #"Gender": 1,  # Male (0 for Female, 1 for Male)
    "Family History": Family_History,  # Present (0 for Absent, 1 for Present)
    "Radiation Exposure": Radiation_Exposure,  # Low (0 for Low, 1 for Moderate, 2 for High)
    "Birth Control": Birth_Control,  # None (0 for None, 1 for Low, 2 for Moderate, 3 for High)
    "Hormone Therapy": Hormone_Therapy,  # Moderate (0 for None, 1 for Low, 2 for Moderate, 3 for High)
    "Alcohol Consumption": Alcohol_Consumption,  # Low (0 for None, 1 for Low, 2 for Moderate, 3 for High)
    "Inherited Gene": Inherited_Gene,  # Absent (0 for Absent, 1 for Present)
    "Previous History": Previous_History,  # None (0 for None, 1 for Present)
    "Hormonal": Hormonal,  # Balanced (0 for Balanced, 1 for Imbalanced)
    "Dense Breast Tissue": Desnse_Breast,  # Present (0 for Absent, 1 for Present)
    "Pregnancy Age": Pregnancy_Age,  # Young (0 for Young, 1 for Middle-aged, 2 for Older)
    "Last Menstrual Cycle Age": Last_Menstrual_Cycle_Age,  # Middle-aged (0 for Young, 1 for Middle-aged, 2 for Older)
    "Menstrual Cycle Age": Menstrual_Cycle_Age,  # Young (0 for Young, 1 for Old)
    "BMI": Bmi,  # Moderate (0 for None, 1 for Low, 2 for Moderate, 3 for High)
}

# Convert the sample input into a DataFrame


if button:
    sample_data = pd.DataFrame([sample_input])
    risk_prediction = clf.predict(sample_data)
    risk_levels = {0: "Low", 1: "Moderate", 2: "High"}
    
    predicted_risk_level = risk_levels[risk_prediction[0]]
    if predicted_risk_level =="Low":
        id = "success"
    elif predicted_risk_level=="Moderate":
        id="warning"
    elif predicted_risk_level=="High":
        id ="danger"
    st.markdown(f"<span class='card btn btn-{id}' style='border-radius:20px; font-size:25px;' ><b>{predicted_risk_level}</b></span>",unsafe_allow_html=True)
    #st.write("risk",predicted_risk_level)
    # Calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    
    st.metric(label="Accuracy", value=accuracy, delta=1.0,
    delta_color="inverse")