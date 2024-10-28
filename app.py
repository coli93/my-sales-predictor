import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression  # Për parashikimin
import numpy as np

# Konfigurimi i faqes
st.set_page_config(page_title="Biznes Menaxhimi", layout="centered")

# Funksioni për autentifikim
def authenticate(username, password):
    return username == "admin" and password == "admin"

# Funksioni i Login-it
def login():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.title("Biznes Menaxhimi - Login")
        username = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.success("Login i suksesshëm!")
            else:
                st.error("Email ose Password i pasaktë!")

# Parashikimi me Inteligjencë Artificiale për Shitjet
def sales_forecast():
    st.header("🔮 Parashikimi Inteligjent i Shitjeve")

    # Testimi fillestar për të dhënat e shitjeve (mund të jenë nga një bazë të dhënash në përdorim real)
    if 'sales_data' not in st.session_state:
        # Fillon me disa të dhëna të thjeshta të shitjeve
        st.session_state['sales_data'] = pd.DataFrame({
            "Muaji": list(range(1, 13)),
            "Shitjet": [2500 * i + 5000 for i in range(1, 13)]
        })

    # Trajnimi i modelit
    data = st.session_state['sales_data']
    X = np.array(data["Muaji"]).reshape(-1, 1)
    y = data["Shitjet"]

    model = LinearRegression()
    model.fit(X, y)  # Modeli mëson nga të dhënat aktuale

    # Futja e numrit të muajve për parashikim
    months = st.number_input("Fut numrin e muajit për parashikim (1-12):", min_value=1, max_value=12, step=1)
    if st.button("Parashiko shitjet"):
        future_months = np.array(range(1, months + 1)).reshape(-1, 1)
        predicted_sales = model.predict(future_months)
        
        st.success(f"Parashikimi për shitjet në {months} muaj është: {predicted_sales[-1]:.2f} €")

        # Grafiku i parashikimit
        plt.figure(figsize=(10, 5))
        plt.plot(data["Muaji"], data["Shitjet"], marker='o', linestyle='-', label="Shitjet Aktual")
        plt.plot(future_months, predicted_sales, marker='x', linestyle='--', label="Parashikimi")
        plt.xlabel("Muajt")
        plt.ylabel("Shitjet (€)")
        plt.title("Parashikimi Inteligjent i Shitjeve")
        plt.legend()
        st.pyplot(plt)

        # Azhurnimi i modelit me të dhëna të reja (auto-learning)
        for i, sale in enumerate(predicted_sales):
            st.session_state['sales_data'] = st.session_state['sales_data'].append(
                {"Muaji": len(data) + i + 1, "Shitjet": sale}, ignore_index=True
            )

# Menaxhimi i Inventarit
def inventory_management():
    st.header("📦 Menaxhimi i Inventarit")
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Emri i Produktit", "Kategori", "Sasia", "Çmimi (€)", "Data e Skadencës"])

    with st.form("add_item_form"):
        item_name = st.text_input("Emri i Produktit")
        item_category = st.selectbox("Kategoria", ["Ushqim", "Pije", "Të Tjera"])
        item_qty = st.number_input("Sasia", min_value=1, step=1)
        item_price = st.number_input("Çmimi (€)", min_value=0.01, step=0.01)
        item_expiry = st.date_input("Data e Skadencës (Opsionale)", value=None)
        submitted = st.form_submit_button("Shto Artikullin")
        
        if submitted:
            new_data = pd.DataFrame([[item_name, item_category, item_qty, item_price, item_expiry]],
                                    columns=["Emri i Produktit", "Kategori", "Sasia", "Çmimi (€)", "Data e Skadencës"])
            st.session_state['inventory'] = pd.concat([st.session_state['inventory'], new_data], ignore_index=True)
            st.success(f"Artikulli '{item_name}' u shtua në inventar!")

    st.subheader("Inventari Aktual")
    st.dataframe(st.session_state['inventory'])

    if not st.session_state['inventory'].empty:
        selected_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(st.session_state['inventory']) - 1, step=1)
        if st.button("Fshi Artikullin"):
            st.session_state['inventory'].drop(index=selected_index, inplace=True)
            st.session_state['inventory'].reset_index(drop=True, inplace=True)
            st.success("Artikulli u fshi me sukses!")

    # Produktet afër skadimit
    st.subheader("Produktet Afër Skadimit")
    try:
        expiring_soon = st.session_state['inventory'][
            (st.session_state['inventory']["Data e Skadencës"].notnull()) &
            (pd.to_datetime(st.session_state['inventory']["Data e Skadencës"]) <= datetime.now() + timedelta(days=7))
        ]
        if not expiring_soon.empty:
            st.warning("Këto produkte do të skadojnë së shpejti:")
            st.dataframe(expiring_soon)
        else:
            st.info("Asnjë produkt nuk është afër skadimit.")
    except Exception as e:
        st.error(f"Gabim gjatë përpunimit të skadencave: {e}")

# Funksioni kryesor për navigimin e aplikacionit
def main():
    login()
    if st.session_state['authenticated']:
        st.sidebar.title("Menuja")
        menu = {
            "Parashikimi i Shitjeve": sales_forecast,
            "Menaxhimi i Inventarit": inventory_management,
        }
        choice = st.sidebar.selectbox("Zgjidh një funksion:", list(menu.keys()))
        menu[choice]()

if __name__ == "__main__":
    main()
