import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Konfigurimi i faqes
st.set_page_config(page_title="Biznes Menaxhimi", layout="centered")

# Funksioni për autentifikim
def authenticate(username, password):
    return username == "admin" and password == "admin"

# Kontroll për autentifikimin
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

def sales_forecast():
    st.header("🔮 Parashikimi i Shitjeve")
    months = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)
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

def inventory_management():
    st.header("📦 Menaxhimi i Inventarit")
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Emri i Produktit", "Kategori", "Sasia", "Çmimi (€)", "Data e Skadencës"])

    # Formulari për shtimin e artikujve në inventar
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

    # Shfaqja e inventarit aktual
    st.subheader("Inventari Aktual")
    st.dataframe(st.session_state['inventory'])

    # Fshirja e artikujve
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

def client_management():
    st.header("👥 Menaxhimi i Klientëve")
    if 'clients' not in st.session_state:
        st.session_state['clients'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])

    with st.form("add_client_form"):
        client_name = st.text_input("Emri")
        client_surname = st.text_input("Mbiemri")
        client_email = st.text_input("Email")
        client_phone = st.text_input("Numri i Telefonit")
        add_client = st.form_submit_button("Shto Klientin")

        if add_client:
            client_data = pd.DataFrame([[client_name, client_surname, client_email, client_phone]], 
                                       columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])
            st.session_state['clients'] = pd.concat([st.session_state['clients'], client_data], ignore_index=True)
            st.success(f"Klienti '{client_name} {client_surname}' u shtua me sukses!")

    # Lista e klientëve
    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])

    # Fshirja e klientëve
    if not st.session_state['clients'].empty:
        client_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(st.session_state['clients']) - 1, step=1)
        if st.button("Fshi Klientin"):
            st.session_state['clients'].drop(index=client_index, inplace=True)
            st.session_state['clients'].reset_index(drop=True, inplace=True)
            st.success("Klienti u fshi me sukses!")

def financial_reports():
    st.header("💲 Raportet Financiare")
    revenue = st.number_input("Të ardhurat mujore (€)", min_value=0.00, step=0.01)
    expenses = st.number_input("Shpenzimet mujore (€)", min_value=0.00, step=0.01)
    
    if st.button("Gjenero Raportin"):
        profit = revenue - expenses
        st.subheader("Raporti Financiar")
        st.write(f"Të ardhurat mujore: €{revenue:.2f}")
        st.write(f"Shpenzimet mujore: €{expenses:.2f}")
        st.write(f"Fitimi: €{profit:.2f}")
        
        if profit > 0:
            st.success("Biznesi është në fitim!")
        elif profit < 0:
            st.error("Biznesi është në humbje!")
        else:
            st.info("Biznesi është në barazim!")

def employee_management():
    st.header("👨‍💼 Menaxhimi i Punonjësve")
    if 'employees' not in st.session_state:
        st.session_state['employees'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])

    with st.form("add_employee_form"):
        employee_name = st.text_input("Emri")
        employee_surname = st.text_input("Mbiemri")
        employee_position = st.text_input("Pozita")
        employee_phone = st.text_input("Numri i Telefonit")
        employee_email = st.text_input("Email")
        add_employee = st.form_submit_button("Shto Punonjësin")
        
        if add_employee:
            employee_data = pd.DataFrame([[employee_name, employee_surname, employee_position, employee_phone, employee_email]], 
                                         columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])
            st.session_state['employees'] = pd.concat([st.session_state['employees'], employee_data], ignore_index=True)
            st.success(f"Punonjësi '{employee_name} {employee_surname}' u shtua me sukses!")

    # Lista e punonjësve
    st.subheader("Lista e Punonjësve")
    st.dataframe(st.session_state['employees'])

    # Fshirja e punonjësve
    if not st.session_state['employees'].empty:
        employee_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(st.session_state['employees']) - 1, step=1)
        if st.button("Fshi Punonjësin"):
            st.session_state['employees'].drop(index=employee_index, inplace=True)
            st.session_state['employees'].reset_index(drop=True, inplace=True)
            st.success("Punonjësi u fshi me sukses!")

# Zgjidhja e funksionit bazuar në zgjedhjen në sidebar
def main():
    login()
    if st.session_state['authenticated']:
        st.sidebar.title("Menuja")
        menu = {
            "Parashikimi i Shitjeve": sales_forecast,
            "Menaxhimi i Inventarit": inventory_management,
            "Menaxhimi i Klientëve": client_management,
            "Raportet Financiare": financial_reports,
            "Menaxhimi i Punonjësve": employee_management
        }
        choice = st.sidebar.selectbox("Zgjidh një funksion:", list(menu.keys()))
        menu[choice]()

if __name__ == "__main__":
    main()
