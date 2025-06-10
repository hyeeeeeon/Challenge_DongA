import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title = "Customer Churn Prediction Dashboard", layout = "wide")

# Dataset load
data_file = "./Results/high_risk_customers.csv"

st.title("Customer Churn Prediction Dashboard")

try:
    df = pd.read_csv(data_file)

except FileNotFoundError:
    st.error("Prediction file not found.")
    st.stop()

# 슬라이더로 확률 기준 설정
threshold = st.slider("Set churn probability threshold", 0.0, 1.0, 0.75, 0.01)

# 기준 이상인 고객만 필터링
high_risk_df = df[df["Churn_Prob"] >= threshold]

# 팝업 경고
if not high_risk_df.empty:
    st.warning(f"🚨 There are {len(high_risk_df)} customers with churn probability >= {threshold:.2f}")

else:
    st.success("No high-risk customers at the moment.")   

# 테이블로 시각화
st.subheader("High-Risk Customer List")
st.dataframe(high_risk_df[['CustomerID', 'Churn_Prob']].reset_index(drop = True))


st.subheader("Churn Probability Distribution")
fig, ax = plt.subplots()
df['Churn_Prob'].hist(bins=20, edgecolor='black', ax=ax)
ax.axvline(threshold, color='red', linestyle='--', label=f'Threshold: {threshold:.2f}')
ax.set_title("Histogram of Churn Probability")
ax.set_xlabel("Churn Probability")
ax.set_ylabel("Number of Customers")
ax.legend()
st.pyplot(fig)