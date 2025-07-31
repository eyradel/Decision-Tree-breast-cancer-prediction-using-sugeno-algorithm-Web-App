# Breast Cancer Prediction System

A comprehensive web application for breast cancer prediction using machine learning algorithms with user authentication and SQLite database storage.

## Features

### User Authentication
- User registration and login system
- Secure password hashing
- Session management
- User-specific prediction history

### Prediction System
- 18 comprehensive symptom inputs
- 7 different breast cancer type predictions
- Confidence scoring
- Risk assessment

### Data Management
- SQLite database for data persistence
- Secure user data storage
- Prediction history tracking
- Export capabilities

## Input Parameters

The system analyzes the following 18 symptoms and characteristics:

1. **Age** - Patient's age
2. **Swollen breast** - Breast swelling
3. **Itching breast** - Breast itching
4. **Swollen lymph nodes** - Lymph node swelling
5. **Nipple pain** - Pain in nipple area
6. **Reddish skin colour** - Skin discoloration
7. **Breast discharge** - Any discharge from breast
8. **Disappearing nipples** - Nipple retraction
9. **Breast temperature** - Elevated breast temperature
10. **Pale appearance breast** - Pale breast appearance
11. **Burning sensation** - Burning feeling in breast
12. **Painful breast** - General breast pain
13. **Lump in the armpit** - Armpit lump detection
14. **Rashes** - Skin rashes on breast
15. **Sores** - Open sores on breast
16. **Thickening** - Breast tissue thickening
17. **Change of shape and size** - Breast shape/size changes
18. **Blood discharge** - Blood discharge from breast

## Output Predictions

The system can predict the following 7 breast cancer types:

1. **Angiosarcoma**
2. **Ductal Carcinoma in situ (DCIS)**
3. **Inflammatory breast cancer**
4. **Invasive lobular carcinoma**
5. **Lobular carcinoma in situ (LCIS)**
6. **Page's disease of the breast**
7. **Recurrent breast cancer**

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Decision-Tree-breast-cancer-prediction-using-sugeno-algorithm-Web-App
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

### First Time Setup
1. Open the application in your web browser
2. Click on the "Register" tab
3. Create a new account with username and password
4. Login with your credentials

### Making Predictions
1. Navigate to the "New Prediction" tab
2. Fill out the comprehensive symptom form
3. Click "Get Prediction" to receive results
4. View detailed prediction with confidence score
5. Results are automatically saved to your history

### Viewing History
1. Go to the "History" tab
2. View all your previous predictions
3. Expand each prediction to see detailed symptoms
4. Track your prediction patterns over time

## Technical Architecture

### Database Schema
- **Users Table**: Stores user authentication data
- **Predictions Table**: Stores all prediction results with symptoms

### Machine Learning Model
- Risk-based scoring algorithm
- Symptom weighting system
- Age factor consideration
- Confidence scoring

### Security Features
- Password hashing using SHA-256
- SQL injection prevention
- Session management
- Data privacy protection

## Important Disclaimer

**Medical Disclaimer**: This application is for educational and screening purposes only. It should not replace professional medical diagnosis or treatment. Always consult with qualified healthcare providers for proper evaluation and treatment.

## Data Privacy

- All data is stored locally in SQLite database
- No data is shared with third parties
- Passwords are securely hashed
- User data is protected and private

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository.

---

**Note**: This application is designed for educational purposes and should be used in conjunction with professional medical advice.