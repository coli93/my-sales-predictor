import streamlit as st
import pandas as pd
from datetime import datetime

# Titulli kryesor i aplikacionit
st.set_page_config(page_title="Biznesi Menaxhimi - All in One", layout="wide")
st.title("Biznesi Menaxhimi - All in One")

# Menuja për të zgjedhur seksionin
menu = ["Parashikimi i Shitjeve", "Menaxhimi i Inventarit", "Menaxhimi i Klientëve", "Raportet Financiare", "Menaxhimi i Punonjësve"]
choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

# Parashikimi i Shitjeve
if choice == "Parashikimi i Shitjeve":
    st.header("🔮 Parashikimi i Shitjeve")
    st.write("Ky seksion ju ndihmon të parashikoni shitjet mujore bazuar në të dhënat ekzistuese.")
    
    # Parashikimi i shitjeve do të shtohet më vonë kur të kompletojmë pjesën e funksionaliteteve.

# Menaxhimi i Inventarit
elif choice == "Menaxhimi i Inventarit":
    st.header("📦 Menaxhimi i Inventarit")
    st.write("Shto, menaxho dhe përditëso inventarin e biznesit tuaj.")

    # Krijo një DataFrame për inventarin (provizor)
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Emri i Artikullit", "Sasia", "Çmimi"])

    # Form për të shtuar artikuj
    with st.form("add_item_form"):
        item_name = st.text_input("Emri i Artikullit")
        item_qty = st.number_input("Sasia", min_value=0, step=1)
        item_price = st.number_input("Çmimi", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Shto Artikullin")

        if submitted:
            new_data = pd.DataFrame([[item_name, item_qty, item_price]], columns=["Emri i Artikullit", "Sasia", "Çmimi"])
            st.session_state['inventory'] = pd.concat([st.session_state['inventory'], new_data], ignore_index=True)
            st.success(f"Artikulli '{item_name}' u shtua në inventar!")

    # Shfaq tabelën e inventarit aktual
    st.subheader("Inventari Aktual")
    st.dataframe(st.session_state['inventory'])
# Menaxhimi i Klientëve
elif choice == "Menaxhimi i Klientëve":
    st.header("👥 Menaxhimi i Klientëve")
    st.write("Mbaj shënim informacionet e klientëve tuaj dhe përditëso të dhënat e tyre.")

    # Krijo një DataFrame për klientët
    if 'clients' not in st.session_state:
        st.session_state['clients'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])

    # Form për të shtuar klientë të rinj
    with st.form("add_client_form"):
        first_name = st.text_input("Emri")
        last_name = st.text_input("Mbiemri")
        email = st.text_input("Email")
        phone_number = st.text_input("Numri i Telefonit")
        submitted = st.form_submit_button("Shto Klientin")

        if submitted:
            new_client = pd.DataFrame([[first_name, last_name, email, phone_number]], columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])
            st.session_state['clients'] = pd.concat([st.session_state['clients'], new_client], ignore_index=True)
            st.success(f"Klienti '{first_name} {last_name}' u shtua me sukses!")

    # Shfaq tabelën e klientëve ekzistues
    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])
    # Shto logjikë për menaxhimin e klientëve këtu...

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💰 Raportet Financiare")
    st.write("Gjenero dhe analizoni raportet financiare të biznesit tuaj.")
    # Logjikë për Raportet Financiare
    
    # Form për të futur të ardhurat dhe shpenzimet
    with st.form("finance_report_form"):
        revenue = st.number_input("Të ardhurat mujore (€)", min_value=0.0, step=0.01)
        expenses = st.number_input("Shpenzimet mujore (€)", min_value=0.0, step=0.01)
        finance_submitted = st.form_submit_button("Gjenero Raportin")

    if finance_submitted:
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
    # Shto logjikë për raportet financiare këtu...

# Menaxhimi i Punonjësve
elif choice == "Menaxhimi i Punonjësve":
    st.header("👷‍♀️ Menaxhimi i Punonjësve")
    st.write("Shto dhe menaxho punonjësit e biznesit tuaj.")
    # Logjikë për Menaxhimin e Punonjësve

    # Ruaj të dhënat e punonjësve në një DataFrame
    if 'employees' not in st.session_state:
        st.session_state['employees'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])

    # Form për të shtuar punonjës të rinj
    with st.form("add_employee_form"):
        emp_first_name = st.text_input("Emri")
        emp_last_name = st.text_input("Mbiemri")
        emp_position = st.text_input("Pozita")
        emp_phone = st.text_input("Numri i Telefonit")
        emp_email = st.text_input("Email")
        emp_submitted = st.form_submit_button("Shto Punonjësin")

    if emp_submitted:
        new_emp_data = pd.DataFrame([[emp_first_name, emp_last_name, emp_position, emp_phone, emp_email]],
                                    columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])
        st.session_state['employees'] = pd.concat([st.session_state['employees'], new_emp_data], ignore_index=True)
        st.success(f"Punonjësi '{emp_first_name} {emp_last_name}' u shtua me sukses!")

    # Shfaq tabelën e punonjësve aktual
    st.subheader("Lista e Punonjësve")
    st.dataframe(st.session_state['employees'])
    # Shto logjikë për menaxhimin e punonjësve këtu...
