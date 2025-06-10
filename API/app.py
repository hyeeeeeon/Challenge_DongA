from flask import Flask, request, jsonify
import pandas as pd
import joblib
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
MANAGER_EMAIL = os.getenv("MANAGER_EMAIL")

# 모델 로딩
model = joblib.load('./Model/logistic_model.pkl')
features = ['AverageViewingDuration', 'ViewingHoursPerWeek', 'MonthlyCharges', 'TotalCharges','AccountAge', 'UserRating', 'ContentDownloadsPerMonth']

# Flask app 선언
app = Flask(__name__)

# e-mail 발송
def send_email(email, customerID, churnPorb):
    msg = MIMEText(f""" 고객 이탈 경고 
        고객 ID: {customerID}
        예측된 이탈 확률: {churnPorb*100:.1f}%
        대응이 필요합니다.""")
    msg['Subject'] = "고객 이탈 위험 알림"
    msg['From'] = EMAIL_ADDRESS       # 기업 이메일 주소
    msg['To'] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/predict', methods = ['POST'])
def predict():
    try:
        data = request.get_json()
        input = pd.DataFrame([data])[features]
        prob = model.predict_proba(input)[0,1]
        
        # email 발송 기준
        if prob >= 0.75:
            # MISSING 인 경우는 CustomerID를 찾을 수 없을 때    
            send_email(MANAGER_EMAIL, data.get("CustomerID", "MISSING"), prob)

        return jsonify({"Churn_Prob": round(float(prob), 4)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def home():
    return "API loading"

if __name__ == '__main__':
    app.run(debug = True)