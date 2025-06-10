import pandas as pd
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

data_path  = "./Data/preprocessing_train.csv"
df = pd.read_csv(data_path)
print("데이터 로드 완료", df.shape)

# 모델 피처 분리
X = df[['AverageViewingDuration', 'ViewingHoursPerWeek', 'MonthlyCharges', 'TotalCharges','AccountAge', 'UserRating', 'ContentDownloadsPerMonth']]
y = df['Churn']

model = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(C = 0.01, penalty = 'l2', max_iter = 1000, random_state = 42))
])
model.fit(X,y)

# 모델 저장
joblib.dump(model, './Model/logistic_model.pkl')
print("모델 저장 완료")

# 테스트 데이터로 확인
test_df = pd.read_csv('./Data/test.csv')
X_test = test_df[['AverageViewingDuration', 'ViewingHoursPerWeek', 'MonthlyCharges', 'TotalCharges','AccountAge', 'UserRating', 'ContentDownloadsPerMonth']]

# 에측
test_df['Churn_Prob'] = model.predict_proba(X_test)[:, 1]

# 이탈 위험 고객 
top_risk = test_df.sort_values(by = 'Churn_Prob', ascending = False)

#결과
print("이탈 위험 고객 TOP 10")
print(top_risk[['CustomerID', 'Churn_Prob']].head(10))

# 저장
top_risk.to_csv('./Results/high_risk_customers.csv', index = False)