import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Vendosja e konfigurimit të faqes në fillim
st.set_page_config(page_title="Menagjimi i Biznesit", layout="centered")

# Funksioni për autentifikim
def authenticate(username, password):
    users = {
        "admin": {"password": "admin", "role": "shefi"},
        "menaxheri": {"password": "menaxheri", "role": "menaxher"},
        "arkatari": {"password": "arkatari", "role": "arkatar"},
        "financa": {"password": "financa", "role": "financa"},
        "marketingu": {"password": "marketingu", "role": "marketing"}
    }
    user = users.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None

# Funksioni për regjistrimin e hyrjes dhe daljes së përdoruesit
def log_performance(username, action):
    now = datetime.now()
    if 'performance_log' not in st.session_state:
        st.session_state['performance_log'] = pd.DataFrame(columns=["User", "Date", "Login Time", "Logout Time", "Duration (Hours)"])

    if action == "login":
        st.session_state['performance_log'] = pd.concat([
            st.session_state['performance_log'],
            pd.DataFrame([[username, now.date(), now, None, None]], columns=["User", "Date", "Login Time", "Logout Time", "Duration (Hours)"])
        ], ignore_index=True)

    elif action == "logout":
        index = st.session_state['performance_log'][(st.session_state['performance_log']["User"] == username) & 
                                                    (st.session_state['performance_log']["Logout Time"].isna())].index[-1]
        login_time = st.session_state['performance_log'].at[index, "Login Time"]
        duration = (now - login_time).total_seconds() / 3600
        st.session_state['performance_log'].at[index, "Logout Time"] = now
        st.session_state['performance_log'].at[index, "Duration (Hours)"] = round(duration, 2)
        save_performance()

# Funksion për të ruajtur performancën në një skedar CSV
def save_performance():
    if 'performance_log' in st.session_state:
        st.session_state['performance_log'].to_csv("performance_log.csv", index=False)

# Lexoni performancën nga CSV nëse ekziston
def load_performance():
    if os.path.exists("performance_log.csv"):
        return pd.read_csv("performance_log.csv")
    return pd.DataFrame(columns=["User", "Date", "Login Time", "Logout Time", "Duration (Hours)"])

# Ruani performancën e mëparshme në `session_state`
st.session_state['performance_log'] = load_performance()

# Kontrollo nëse përdoruesi është autentifikuar
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None

# Nëse përdoruesi nuk është autentifikuar, shfaq faqen e login-it
if not st.session_state['authenticated']:
    st.title("Biznesi Menaxhimi - Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state['authenticated'] = True
            st.session_state['role'] = role
            st.session_state['username'] = username
            st.success(f"Login i suksesshëm si {role}!")
            log_performance(username, "login")
        else:
            st.error("Email ose Password i pasaktë!")
else:
    # Paneli kryesor për të treguar përmbledhje
    st.title("Menagjimi i Biznesit - Paneli Kryesor")
    
    # Seksioni i përmbledhjes
    col1, col2, col3 = st.columns(3)
    with col1:
        total_sales = 20000  # Ky është një shembull i të dhënave
        st.metric("Të Ardhurat Mujore (€)", f"{total_sales:.2f}")
    with col2:
        total_products = len(st.session_state.get('inventory', []))
        st.metric("Numri i Produkteve", total_products)
    with col3:
        total_users = len(st.session_state['performance_log']['User'].unique())
        st.metric("Punonjës Aktiv", total_users)

    # Menuja për të zgjedhur seksionin
    menu = [
        "Parashikimi i Shitjeve", 
        "Menaxhimi i Inventarit", 
        "Raportet e Performancës",
        "Dil"
    ]
    choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

    # Parashikimi i Shitjeve, Menaxhimi i Inventarit dhe të tjera janë të njëjta si më parë...
    
    # Butoni për Daljen
    elif choice == "Dil":
        st.session_state['authenticated'] = False
        if st.session_state['username']:
            log_performance(st.session_state['username'], "logout")
        st.session_state.clear()  # Pastron të gjithë sesionin
        st.experimental_rerun()
