import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Vendosja e konfigurimit të faqes në fillim
st.set_page_config(page_title="Menagjimi i Biznesit", layout="centered")

# Funksioni për autentifikim
def authenticate(username, password):
    return username == "admin" and password == "admin"

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
        # Gjeni rreshtin e fundit ku përdoruesi ka bërë login, dhe shtoni kohën e daljes
        index = st.session_state['performance_log'][(st.session_state['performance_log']["User"] == username) & 
                                                    (st.session_state['performance_log']["Logout Time"].isna())].index[-1]
        login_time = st.session_state['performance_log'].at[index, "Login Time"]
        duration = (now - login_time).total_seconds() / 3600  # Kalkulo kohën në orë
        st.session_state['performance_log'].at[index, "Logout Time"] = now
        st.session_state['performance_log'].at[index, "Duration (Hours)"] = round(duration, 2)

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
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Login i suksesshëm!")
            log_performance(username, "login")
        else:
            st.error("Email ose Password i pasaktë!")
else:
    # Pjesa kryesore e aplikacionit pas autentifikimit
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            max-width: 90%;
            padding-left: 5%;
            padding-right: 5%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Menagjimi i Biznesit")

    # Menuja për të zgjedhur seksionin
    menu = [
        "Parashikimi i Shitjeve", 
        "Menaxhimi i Inventarit", 
        "Raportet e Performancës",  # Shto seksionin e raporteve
        "Dil"
    ]
    choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

    # Parashikimi i Shitjeve
    if choice == "Parashikimi i Shitjeve":
        st.header("🔮 Parashikimi i Shitjeve")
        st.write("Ky seksion ju ndihmon të parashikoni shitjet e ardhshme bazuar në të dhënat ekzistuese.")
        
        # Fut numrin e muajve për parashikim
        months = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)
        
        # Butoni për të gjeneruar parashikimin e shitjeve
        if st.button("Parashiko shitjet"):
            sales = months * 2500 + 5000
            st.success(f"Parashikimi për shitjet është: {sales:.2f} €")
            
            # Grafiku i parashikimit
            x = list(range(1, months + 1))
            y = [i * 2500 + 5000 for i in x]
            plt.figure(figsize=(10, 5))
            plt.plot(x, y, marker='o', linestyle='-', color='b')
            plt.xlabel("Muajt")
            plt.ylabel("Shitjet (€)")
            plt.title("Parashikimi i Shitjeve")
            plt.grid(True)
            st.pyplot(plt)

    # Menaxhimi i Inventarit
    elif choice == "Menaxhimi i Inventarit":
        st.header("📦 Menaxhimi i Inventarit")
        if 'inventory' not in st.session_state:
            st.session_state['inventory'] = pd.DataFrame(columns=["Emri i Produktit", "Kategori", "Sasia", "Çmimi (€)", "Data e Skadencës"])
        
        # Shto artikuj të rinj në inventar
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
        inventory_df = st.session_state['inventory']
        st.dataframe(inventory_df)

        if not inventory_df.empty:
            selected_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(inventory_df) - 1, step=1)
            if st.button("Fshi Artikullin"):
                st.session_state['inventory'].drop(index=selected_index, inplace=True)
                st.session_state['inventory'].reset_index(drop=True, inplace=True)
                st.success("Artikulli u fshi me sukses!")

        # Kontrollo produktet afër skadimit dhe lajmëro përdoruesin
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

    # Raportet e Performancës
    elif choice == "Raportet e Performancës":
        st.header("📊 Raportet e Performancës")
        st.write("Shfaq raportet ditore dhe mujore të performancës së punonjësve.")
        if 'performance_log' in st.session_state:
            # Raporti ditor
            st.subheader("Raporti Ditor")
            today = datetime.now().date()
            daily_report = st.session_state['performance_log'][st.session_state['performance_log']["Date"] == today]
            st.write(daily_report)

            # Raporti mujor
            st.subheader("Raporti Mujor")
            month_start = datetime.now().replace(day=1).date()
            monthly_report = st.session_state['performance_log'][st.session_state['performance_log']["Date"] >= month_start]
            st.write(monthly_report)

    # Butoni për Daljen
    elif choice == "Dil":
        st.session_state['authenticated'] = False
        if st.session_state['username']:
            log_performance(st.session_state['username'], "logout")
        st.experimental_rerun()
