import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from datetime import datetime

# Të dhënat shembull për modelin
data = pd.DataFrame({
    'Month_Num': range(1, 13),
    'Sales': [24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000]
})

# Shto veçori të reja
data['Month'] = [(datetime(2023, m, 1)).month for m in data['Month_Num']]
data['Season'] = data['Month'].apply(lambda x: (x % 12 + 3) // 3)

# Krijo variablat X dhe y
X = data[['Month_Num', 'Month', 'Season']]
y = data['Sales']

# Trajno modelin
model = LinearRegression()
model.fit(X, y)

# Funksion për parashikimin
def predict_sales(month_num):
    month = (datetime(2023, month_num, 1)).month
    season = (month % 12 + 3) // 3
    X_new = np.array([[month_num, month, season]])
    prediction = model.predict(X_new)
    return prediction[0]

# Titulli dhe përshkrimi
st.title("📈 Parashikuesi i Shitjeve për Bizneset")
st.write("Ky aplikacion ndihmon në parashikimin e shitjeve mujore për bizneset bazuar në të dhënat ekzistuese.")

# Input nga përdoruesi
month_num = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)

if st.button("🔮 Parashiko shitjet"):
    prediction = predict_sales(month_num)
    st.success(f"Parashikimi për shitjet është: {prediction:.2f}")

    # Grafikë
    st.line_chart(data['Sales'])

# Informacion shtesë për përdoruesin
st.info("Ju lutem futni një numër muaji nga 1 deri në 12 për të parë parashikimin e shitjeve.")
