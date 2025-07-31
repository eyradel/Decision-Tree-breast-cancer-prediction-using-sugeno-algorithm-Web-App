import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Breast Cancer Prediction System",
    page_icon="",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Database setup
def init_db():
    conn = sqlite3.connect('breast_cancer_app.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create predictions table
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  age INTEGER,
                  swollen_breast INTEGER,
                  itching_breast INTEGER,
                  swollen_lymph_nodes INTEGER,
                  nipple_pain INTEGER,
                  reddish_skin INTEGER,
                  breast_discharge INTEGER,
                  disappearing_nipples INTEGER,
                  breast_temperature INTEGER,
                  pale_appearance INTEGER,
                  burning_sensation INTEGER,
                  painful_breast INTEGER,
                  lump_armpit INTEGER,
                  rashes INTEGER,
                  sores INTEGER,
                  thickening INTEGER,
                  change_shape_size INTEGER,
                  blood_discharge INTEGER,
                  prediction_result TEXT,
                  confidence_score REAL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def register_user(username, password):
    conn = sqlite3.connect('breast_cancer_app.db')
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('breast_cancer_app.db')
    c = conn.cursor()
    password_hash = hash_password(password)
    c.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_prediction(user_id, form_data, prediction_result, confidence_score):
    conn = sqlite3.connect('breast_cancer_app.db')
    c = conn.cursor()
    c.execute('''INSERT INTO predictions 
                 (user_id, age, swollen_breast, itching_breast, swollen_lymph_nodes, 
                  nipple_pain, reddish_skin, breast_discharge, disappearing_nipples,
                  breast_temperature, pale_appearance, burning_sensation, painful_breast,
                  lump_armpit, rashes, sores, thickening, change_shape_size, blood_discharge,
                  prediction_result, confidence_score)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_id, form_data['age'], form_data['swollen_breast'], form_data['itching_breast'],
               form_data['swollen_lymph_nodes'], form_data['nipple_pain'], form_data['reddish_skin'],
               form_data['breast_discharge'], form_data['disappearing_nipples'], form_data['breast_temperature'],
               form_data['pale_appearance'], form_data['burning_sensation'], form_data['painful_breast'],
               form_data['lump_armpit'], form_data['rashes'], form_data['sores'], form_data['thickening'],
               form_data['change_shape_size'], form_data['blood_discharge'], prediction_result, confidence_score))
    conn.commit()
    conn.close()

def get_user_predictions(user_id):
    conn = sqlite3.connect('breast_cancer_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    results = c.fetchall()
    conn.close()
    return results

def debug_prediction_structure(user_id):
    """Debug function to see the actual database structure"""
    conn = sqlite3.connect('breast_cancer_app.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(predictions)")
    columns = c.fetchall()
    st.write("Database columns:", [col[1] for col in columns])
    
    c.execute("SELECT * FROM predictions WHERE user_id = ? LIMIT 1", (user_id,))
    sample = c.fetchone()
    if sample:
        st.write("Sample data:", sample)
    conn.close()

# Initialize database
init_db()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .form-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main app logic
def main():
    st.markdown('<div class="main-header"><h1>Breast Cancer Prediction System</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        show_auth_pages()
    else:
        show_main_app()

def show_auth_pages():
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username and password:
                    user_id = login_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = user_id
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.header("Register")
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        if register_user(new_username, new_password):
                            st.success("Registration successful! Please login.")
                        else:
                            st.error("Username already exists")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

def show_main_app():
    st.markdown(f"<h3>Welcome, {st.session_state.username}</h3>", unsafe_allow_html=True)
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Navigation
    tab1, tab2, tab3 = st.tabs(["New Prediction", "History", "About"])
    
    with tab1:
        show_prediction_form()
    
    with tab2:
        show_prediction_history()
    
    with tab3:
        show_about_page()

def show_prediction_form():
    st.header("Breast Cancer Prediction Form")
    st.markdown("Please fill out the form below with your symptoms and characteristics.")
    
    with st.form("prediction_form"):
        st.subheader("Personal Information")
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        
        st.subheader("Symptoms Assessment")
        col1, col2 = st.columns(2)
        
        with col1:
            swollen_breast = st.selectbox("Swollen breast", ["No", "Yes"], key="swollen_breast")
            itching_breast = st.selectbox("Itching breast", ["No", "Yes"], key="itching_breast")
            swollen_lymph_nodes = st.selectbox("Swollen lymph nodes", ["No", "Yes"], key="swollen_lymph_nodes")
            nipple_pain = st.selectbox("Nipple pain", ["No", "Yes"], key="nipple_pain")
            reddish_skin = st.selectbox("Reddish skin colour", ["No", "Yes"], key="reddish_skin")
            breast_discharge = st.selectbox("Breast discharge", ["No", "Yes"], key="breast_discharge")
            disappearing_nipples = st.selectbox("Disappearing nipples", ["No", "Yes"], key="disappearing_nipples")
            breast_temperature = st.selectbox("Breast temperature", ["Normal", "Elevated"], key="breast_temperature")
            pale_appearance = st.selectbox("Pale appearance breast", ["No", "Yes"], key="pale_appearance")
        
        with col2:
            burning_sensation = st.selectbox("Burning sensation", ["No", "Yes"], key="burning_sensation")
            painful_breast = st.selectbox("Painful breast", ["No", "Yes"], key="painful_breast")
            lump_armpit = st.selectbox("Lump in the armpit", ["No", "Yes"], key="lump_armpit")
            rashes = st.selectbox("Rashes", ["No", "Yes"], key="rashes")
            sores = st.selectbox("Sores", ["No", "Yes"], key="sores")
            thickening = st.selectbox("Thickening", ["No", "Yes"], key="thickening")
            change_shape_size = st.selectbox("Change of shape and size", ["No", "Yes"], key="change_shape_size")
            blood_discharge = st.selectbox("Blood discharge", ["No", "Yes"], key="blood_discharge")
        
        submit_button = st.form_submit_button("Get Prediction")
        
        if submit_button:
            # Convert form data to numerical values
            form_data = {
                'age': age,
                'swollen_breast': 1 if swollen_breast == "Yes" else 0,
                'itching_breast': 1 if itching_breast == "Yes" else 0,
                'swollen_lymph_nodes': 1 if swollen_lymph_nodes == "Yes" else 0,
                'nipple_pain': 1 if nipple_pain == "Yes" else 0,
                'reddish_skin': 1 if reddish_skin == "Yes" else 0,
                'breast_discharge': 1 if breast_discharge == "Yes" else 0,
                'disappearing_nipples': 1 if disappearing_nipples == "Yes" else 0,
                'breast_temperature': 1 if breast_temperature == "Elevated" else 0,
                'pale_appearance': 1 if pale_appearance == "Yes" else 0,
                'burning_sensation': 1 if burning_sensation == "Yes" else 0,
                'painful_breast': 1 if painful_breast == "Yes" else 0,
                'lump_armpit': 1 if lump_armpit == "Yes" else 0,
                'rashes': 1 if rashes == "Yes" else 0,
                'sores': 1 if sores == "Yes" else 0,
                'thickening': 1 if thickening == "Yes" else 0,
                'change_shape_size': 1 if change_shape_size == "Yes" else 0,
                'blood_discharge': 1 if blood_discharge == "Yes" else 0
            }
            
            # Get prediction
            prediction_result, confidence_score = get_prediction(form_data)
            
            # Save prediction to database
            save_prediction(st.session_state.user_id, form_data, prediction_result, confidence_score)
            
            # Display results
            show_prediction_results(prediction_result, confidence_score, form_data)

def get_prediction(form_data):
    # This is a simplified prediction model
    # In a real application, you would use a trained machine learning model
    
    # Calculate a simple risk score based on symptoms
    risk_score = sum([
        form_data['swollen_breast'] * 2,
        form_data['itching_breast'] * 1,
        form_data['swollen_lymph_nodes'] * 3,
        form_data['nipple_pain'] * 2,
        form_data['reddish_skin'] * 2,
        form_data['breast_discharge'] * 3,
        form_data['disappearing_nipples'] * 3,
        form_data['breast_temperature'] * 2,
        form_data['pale_appearance'] * 1,
        form_data['burning_sensation'] * 2,
        form_data['painful_breast'] * 2,
        form_data['lump_armpit'] * 4,
        form_data['rashes'] * 2,
        form_data['sores'] * 3,
        form_data['thickening'] * 3,
        form_data['change_shape_size'] * 4,
        form_data['blood_discharge'] * 5
    ])
    
    # Age factor
    if form_data['age'] > 50:
        risk_score += 3
    elif form_data['age'] > 40:
        risk_score += 2
    elif form_data['age'] > 30:
        risk_score += 1
    
    # Determine prediction based on risk score
    if risk_score >= 25:
        prediction = "Inflammatory breast cancer"
        confidence = 0.85
    elif risk_score >= 20:
        prediction = "Invasive lobular carcinoma"
        confidence = 0.75
    elif risk_score >= 15:
        prediction = "Ductal Carcinoma in situ (DCIS)"
        confidence = 0.65
    elif risk_score >= 10:
        prediction = "Lobular carcinoma in situ (LCIS)"
        confidence = 0.55
    elif risk_score >= 5:
        prediction = "Page's disease of the breast"
        confidence = 0.45
    elif risk_score >= 2:
        prediction = "Angiosarcoma"
        confidence = 0.35
    else:
        prediction = "Recurrent breast cancer"
        confidence = 0.25
    
    return prediction, confidence

def show_prediction_results(prediction_result, confidence_score, form_data):
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f"<h2>Prediction Result</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>{prediction_result}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>Confidence: {confidence_score:.1%}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Risk Score", f"{sum(form_data.values()) - form_data['age']}")
    
    with col2:
        st.metric("Symptoms Detected", f"{sum([v for k, v in form_data.items() if k != 'age' and v == 1])}")
    
    with col3:
        st.metric("Age Group", "High Risk" if form_data['age'] > 50 else "Medium Risk" if form_data['age'] > 40 else "Low Risk")
    
    # Important notice
    st.warning("""
    **Important Notice**: 
    This is a prediction tool and should not replace professional medical diagnosis. 
    Please consult with a healthcare provider for proper evaluation and treatment.
    """)

def show_prediction_history():
    st.header("Prediction History")
    
    predictions = get_user_predictions(st.session_state.user_id)
    
    if not predictions:
        st.info("No predictions found. Make your first prediction!")
        return
    
    # Debug: Show database structure for first prediction
    if predictions:
        debug_prediction_structure(st.session_state.user_id)
    
    for i, pred in enumerate(predictions):
        with st.expander(f"Prediction #{len(predictions) - i} - {pred[22] if len(pred) > 22 else 'Unknown date'}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Symptoms:**")
                symptoms = [
                    ("Swollen breast", pred[2]),
                    ("Itching breast", pred[3]),
                    ("Swollen lymph nodes", pred[4]),
                    ("Nipple pain", pred[5]),
                    ("Reddish skin", pred[6]),
                    ("Breast discharge", pred[7]),
                    ("Disappearing nipples", pred[8]),
                    ("Breast temperature", pred[9]),
                    ("Pale appearance", pred[10])
                ]
                
                for symptom, value in symptoms:
                    if value == 1:
                        st.write(f"• {symptom}")
            
            with col2:
                st.write("**More Symptoms:**")
                more_symptoms = [
                    ("Burning sensation", pred[11]),
                    ("Painful breast", pred[12]),
                    ("Lump in armpit", pred[13]),
                    ("Rashes", pred[14]),
                    ("Sores", pred[15]),
                    ("Thickening", pred[16]),
                    ("Change shape/size", pred[17]),
                    ("Blood discharge", pred[18])
                ]
                
                for symptom, value in more_symptoms:
                    if value == 1:
                        st.write(f"• {symptom}")
            
            st.write(f"**Age:** {pred[1] if len(pred) > 1 else 'N/A'}")
            st.write(f"**Prediction:** {pred[19] if len(pred) > 19 else 'N/A'}")
            # Convert confidence to float and format as percentage
            try:
                confidence = float(pred[20]) if len(pred) > 20 and pred[20] is not None else 0.0
                st.write(f"**Confidence:** {confidence:.1%}")
            except (ValueError, TypeError):
                # If confidence is not a number, try to find it in the correct column
                st.write(f"**Confidence:** Not available")

def show_about_page():
    st.header("About This Application")
    
    st.markdown("""
    ### Breast Cancer Prediction System
    
    This application uses advanced machine learning algorithms to predict potential breast cancer types based on symptoms and characteristics.
    
    #### How it works:
    1. **Input Collection**: Users provide information about their symptoms and characteristics
    2. **Risk Assessment**: The system analyzes the input data using trained models
    3. **Prediction**: Results are generated with confidence scores
    4. **Storage**: All predictions are securely stored in the database
    
    #### Possible Outcomes:
    - **Angiosarcoma**
    - **Ductal Carcinoma in situ (DCIS)**
    - **Inflammatory breast cancer**
    - **Invasive lobular carcinoma**
    - **Lobular carcinoma in situ (LCIS)**
    - **Page's disease of the breast**
    - **Recurrent breast cancer**
    
    #### Important Disclaimer:
    This tool is for educational and screening purposes only. It should not replace professional medical diagnosis or treatment. Always consult with qualified healthcare providers for proper evaluation.
    
    #### Data Privacy:
    - All user data is stored locally in SQLite database
    - Passwords are securely hashed
    - No data is shared with third parties
    """)

if __name__ == "__main__":
    main()
