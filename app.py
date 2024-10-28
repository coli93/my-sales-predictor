import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Konfigurimi i faqes
st.set_page_config(page_title="Platforma Inteligjente e Menaxhimit të Biznesit", layout="wide")

# Funksioni i autentifikimit
def authenticate(username, password):
    # Përdoruesit mund të ruhen në një bazë të dhënash në praktikë
    return username == "admin" and password == "admin"

# Funksioni për login
def login():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.title("Platforma Inteligjente e Menaxhimit të Biznesit")
        username = st.text_input("Përdoruesi")
        password = st.text_input("Fjalëkalimi", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.success("Login i suksesshëm!")
            else:
                st.error("Përdorues ose fjalëkalim i pasaktë!")

# Moduli i Parashikimit Inteligjent të Shitjeve
def sales_forecast():
    st.header("🔮 Parashikimi Inteligjent i Shitjeve")
    
    # Testi fillestar për të dhëna, mund të zëvendësohet me të dhëna reale
    if 'sales_data' not in st.session_state:
        st.session_state['sales_data'] = pd.DataFrame({
            "Muaji": np.arange(1, 13),
            "Shitjet": [3000 + 500 * i for i in range(1, 13)]
        })

    # Trajnimi i modelit Linear Regression për të bërë parashikimin e shitjeve
    sales_data = st.session_state['sales_data']
    X = np.array(sales_data["Muaji"]).reshape(-1, 1)
    y = sales_data["Shitjet"]
    
    model = LinearRegression()
    model.fit(X, y)

    months = st.number_input("Fut numrin e muajve për parashikim:", min_value=1, max_value=12)
    if st.button("Parashiko"):
        future_months = np.arange(len(sales_data) + 1, len(sales_data) + months + 1).reshape(-1, 1)
        predictions = model.predict(future_months)
        
        # Azhurnon të dhënat me parashikimet për të mësuar vetë nga të dhënat e reja
        for i, prediction in enumerate(predictions):
            st.session_state['sales_data'] = st.session_state['sales_data'].append(
                {"Muaji": len(sales_data) + i + 1, "Shitjet": prediction}, ignore_index=True
            )
        
        # Vizualizimi i parashikimeve
        st.line_chart(st.session_state['sales_data'].set_index("Muaji"))

# Moduli i Menaxhimit të Inventarit
def inventory_management():
    st.header("📦 Menaxhimi Inteligjent i Inventarit")

    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Produkt", "Kategori", "Sasia", "Çmimi (€)", "Data Skadencës"])

    # Formular për shtimin e produkteve
    with st.form("add_inventory_form"):
        product_name = st.text_input("Emri i Produktit")
        category = st.selectbox("Kategoria", ["Ushqim", "Pije", "Të Tjera"])
        quantity = st.number_input("Sasia", min_value=1)
        price = st.number_input("Çmimi (€)", min_value=0.01, step=0.01)
        expiry_date = st.date_input("Data e Skadencës (Opsionale)")
        add_product = st.form_submit_button("Shto Produktin")

        if add_product:
            new_product = pd.DataFrame([[product_name, category, quantity, price, expiry_date]],
                                       columns=["Produkt", "Kategori", "Sasia", "Çmimi (€)", "Data Skadencës"])
            st.session_state['inventory'] = pd.concat([st.session_state['inventory'], new_product], ignore_index=True)
            st.success(f"Produkti '{product_name}' u shtua me sukses!")

    # Lista e inventarit aktual
    st.dataframe(st.session_state['inventory'])

    # Trego produktet që skadojnë brenda 7 ditëve
    if not st.session_state['inventory'].empty:
        st.subheader("Produktet Afër Skadencës")
        soon_expiring = st.session_state['inventory'][
            pd.to_datetime(st.session_state['inventory']["Data Skadencës"]) <= datetime.now() + timedelta(days=7)
        ]
        st.table(soon_expiring)

# Moduli i Menaxhimit të Klientëve
def client_management():
    st.header("👥 Menaxhimi i Klientëve")
    if 'clients' not in st.session_state:
        st.session_state['clients'] = pd.DataFrame(columns=["Emër", "Mbiemër", "Email", "Telefoni"])

    with st.form("add_client_form"):
        first_name = st.text_input("Emri")
        last_name = st.text_input("Mbiemri")
        email = st.text_input("Email")
        phone = st.text_input("Numri i Telefonit")
        add_client = st.form_submit_button("Shto Klientin")
        
        if add_client:
            new_client = pd.DataFrame([[first_name, last_name, email, phone]],
                                      columns=["Emër", "Mbiemër", "Email", "Telefoni"])
            st.session_state['clients'] = pd.concat([st.session_state['clients'], new_client], ignore_index=True)
            st.success(f"Klienti '{first_name} {last_name}' u shtua me sukses!")
    
    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])

# Moduli i Raporteve Financiare
def financial_reports():
    st.header("💰 Raportet Financiare")
    
    revenue = st.number_input("Të ardhurat mujore (€):", min_value=0.00, step=0.01)
    expenses = st.number_input("Shpenzimet mujore (€):", min_value=0.00, step=0.01)

    if st.button("Gjenero Raportin Financiar"):
        profit = revenue - expenses
        st.metric("Fitimi", f"{profit:.2f} €")
        
        if profit > 0:
            st.success("Biznesi është në fitim!")
        elif profit < 0:
            st.error("Biznesi është në humbje!")
        else:
            st.info("Biznesi është në barazim!")

# Funksioni kryesor për aplikacionin
def main():
    login()
    if st.session_state['authenticated']:
        st.sidebar.title("Menuja e Biznesit Inteligjent")
        modules = {
            "Parashikimi i Shitjeve": sales_forecast,
            "Menaxhimi i Inventarit": inventory_management,
            "Menaxhimi i Klientëve": client_management,
            "Raportet Financiare": financial_reports,
        }
        choice = st.sidebar.selectbox("Zgjidh një funksion:", list(modules.keys()))
        modules[choice]()

if __name__ == "__main__":
    main()
