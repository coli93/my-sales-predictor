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

# Titulli i aplikacionit
st.title("Parashikuesi i Shitjeve për Bizneset")

# Kërko muajin, sezonin dhe numrin e muajit
month_num = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)
season = (month_num % 12 + 3) // 3  # Llogarit sezonin automatikisht

# Parashiko shitjet
if st.button("Parashiko shitjet"):
    future_data = pd.DataFrame({
        'Month_Num': [len(data) + 1],
        'Month': [month_num],
        'Season': [season]
    })
    prediction = model.predict(future_data)[0]
    st.write(f"Parashikimi për shitjet është: {prediction:.2f}")

# Grafika e të dhënave
st.line_chart(data.set_index('Month_Num')['Sales'])
