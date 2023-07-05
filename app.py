import streamlit as st
#funcrions

# Step 2: Define the function to predict cancer aggressiveness
def predict_cancer_aggressiveness(female_age, gender, bmi, age_at_first_pregnancy, family_history, radiation_exposure, birth_control_drugs, age_at_first_menstrual_cycle, age_at_last_menstrual_cycle, postmenopausal_hormone_therapy, alcohol_intake, inherited_gene_mutation, previous_history, hormonal, dense_breast_tissue, obesity):
    # Define the rules based on the relationships between the variables
    # Make predictions based on the rules and st.text_input values
    female_age = 0
    # Rule 1: Higher  for females over 50 years old
    if int(female_age) > 50:
        return "High "
    
    # Rule 2: Higher  for females with family history and dense breast tissue
    if family_history == "Yes" and dense_breast_tissue == "Yes":
        return "High "
    
    # Rule 3: Higher  for females with early age at first menstrual cycle and hormonal factors
    if int(age_at_first_menstrual_cycle) < 12 and hormonal == "Yes":
        return "High "
    
    # Rule 4: Higher  for females with obesity and alcohol consumption
    if int(bmi) >= 30 and alcohol_intake == "High":
        return "High "
    
    # Rule 5: Higher  for females with inherited gene mutations and previous history
    if inherited_gene_mutation == "Yes" and previous_history == "Yes":
        return "High "
    
    # Default rule: Low 
    return "Low "

   

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
            female_age = st.text_input("Enter female's age: ")
            gender = st.text_input("Enter gender: ")
            bmi = st.text_input("Enter BMI: ")
            age_at_first_pregnancy = st.text_input("Enter age at first pregnancy: ")
            family_history = st.text_input("Enter family history (Yes/No): ")
        
    with col2:
        
        with st.expander("#2"):
    
            birth_control_drugs = st.text_input("Enter use of birth control drugs (Yes/No): ")
            age_at_first_menstrual_cycle = st.text_input("Enter age at first menstrual cycle: ")
            age_at_last_menstrual_cycle = st.text_input("Enter age at last menstrual cycle: ")
            postmenopausal_hormone_therapy = st.text_input("Enter postmenopausal hormone therapy (Yes/No): ")
            alcohol_intake = st.text_input("Enter alcohol intake (Low/Moderate/High): ")
    with col3:
        with st.expander("#3"):
            inherited_gene_mutation = st.text_input("Enter inherited gene mutation (Yes/No): ")
            previous_history = st.text_input("Enter previous history (Yes/No): ")
            hormonal = st.text_input("Enter hormonal factors (Yes/No): ")
            dense_breast_tissue = st.text_input("Enter dense breast tissue (Yes/No): ")
            obesity = st.text_input("Enter obesity (Yes/No): ")
    radiation_exposure = st.select_slider("Enter radiation exposure (Low/Moderate/High): ",["Low","Moderate","High"])
    button = st.form_submit_button("click")
# if not (female_age,gender,bmi,age_at_first_menstrual_cycle,family_history,birth_control_drugs,age_at_first_pregnancy,age_at_last_menstrual_cycle,postmenopausal_hormone_therapy,alcohol_intake,inherited_gene_mutation,previous_history,hormonal,dense_breast_tissue,obesity):
#     st.markdown(f"<h2 style='margin-left:-130px; ' class=' btn alert alert-danger'>input is required</h2>",unsafe_allow_html=True)
if button:
    prediction = predict_cancer_aggressiveness(female_age, gender, bmi, age_at_first_pregnancy, family_history, radiation_exposure, birth_control_drugs, age_at_first_menstrual_cycle, age_at_last_menstrual_cycle, postmenopausal_hormone_therapy, alcohol_intake, inherited_gene_mutation, previous_history, hormonal, dense_breast_tissue, obesity)
    st.markdown(f"<h2 style='margin-left:-130px; ' class=' btn alert alert-danger'>{prediction}</h2>",unsafe_allow_html=True)
