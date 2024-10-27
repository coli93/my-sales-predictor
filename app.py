import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Titulli kryesor i aplikacionit
st.set_page_config(page_title="Biznesi Menaxhimi – All in One")
st.title("Biznesi Menaxhimi - All in One")

# Menyja për të zgjedhur seksionin
menu = ["Parashikimi i Shitjeve", "Menaxhimi i Inventarit", "Menaxhimi i Klientëve", "Raportet Financiare", "Menaxhimi i Punonjësve"]
choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

# Parashikimi i Shitjeve
if choice == "Parashikimi i Shitjeve":
    st.header("🔮 Parashikimi i Shitjeve")
    st.write("Ky seksion ju ndihmon të parashikoni shitjet e ardhshme të biznesit tuaj bazuar në të dhënat ekzistuese.")
    
    # Shto input për muajt dhe gjenero parashikimin e shitjeve
    months = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)
    if st.button("Parashiko shitjet"):
        sales_prediction = 25000 + (months * 1000)
        st.write(f"Parashikimi për shitjet është: {sales_prediction:.2f}")

# Menaxhimi i Inventarit
elif choice == "Menaxhimi i Inventarit":
    st.header("📦 Menaxhimi i Inventarit")
    st.write("Shto, menaxho dhe përditëso inventarin e biznesit tuaj.")

    # Krijo një DataFrame për inventarin nëse nuk ekziston
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Emri i Artikullit", "Sasia", "Çmimi"])

    # Form për të shtuar artikuj
    with st.form("add_item_form"):
        item_name = st.text_input("Emri i Artikullit")
        item_qty = st.number_input("Sasia", min_value=0, step=1)
        item_price = st.number_input("Çmimi (€)", min_value=0.0, step=0.1)
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
    st.write("Mbaj shënim informacionet e klientëve të biznesit tuaj.")
    
    # Krijo DataFrame për klientët nëse nuk ekziston
    if 'clients' not in st.session_state:
        st.session_state['clients'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])

    # Form për të shtuar klientë
    with st.form("add_client_form"):
        first_name = st.text_input("Emri")
        last_name = st.text_input("Mbiemri")
        email = st.text_input("Email")
        phone = st.text_input("Numri i Telefonit")
        client_submitted = st.form_submit_button("Shto Klientin")

        if client_submitted:
            new_client = pd.DataFrame([[first_name, last_name, email, phone]], columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])
            st.session_state['clients'] = pd.concat([st.session_state['clients'], new_client], ignore_index=True)
            st.success(f"Klienti '{first_name} {last_name}' u shtua me sukses!")

    # Shfaq tabelën e klientëve aktual
    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💰 Raportet Financiare")
    st.write("Gjenero dhe analizoni raportet financiare të biznesit tuaj.")

    # Shto inputet për të ardhurat dhe shpenzimet
    income = st.number_input("Të ardhurat mujore (€)", min_value=0.00, value=0.00, step=10.00)
    expenses = st.number_input("Shpenzimet mujore (€)", min_value=0.00, value=0.00, step=10.00)
    submitted_report = st.button("Gjenero Raportin")

    if submitted_report:
        # Kalkulo fitimin
        profit = income - expenses
        st.subheader("Raporti Financiar")
        st.write(f"Të ardhurat mujore: €{income:.2f}")
        st.write(f"Shpenzimet mujore: €{expenses:.2f}")
        st.write(f"Fitimi: €{profit:.2f}")
        
        if profit > 0:
            st.success("Biznesi është në fitim!")
        elif profit < 0:
            st.error("Biznesi është në humbje!")
        else:
            st.warning("Biznesi është në ekuilibër!")

        # Vizualizim me grafikë
        months = ["Janar", "Shkurt", "Mars", "Prill", "Maj", "Qershor", "Korrik", "Gusht", "Shtator", "Tetor", "Nëntor", "Dhjetor"]
        profits = [profit] * 12  # Për shembull, duke treguar të njëjtin fitim për çdo muaj për thjeshtësi.

        fig, ax = plt.subplots()
        ax.plot(months, profits, marker='o')
        ax.set_title("Fitimi Mujore gjatë Vitit")
        ax.set_xlabel("Muajt")
        ax.set_ylabel("Fitimi (€)")
        ax.grid(True)
        st.pyplot(fig)

# Menaxhimi i Punonjësve
elif choice == "Menaxhimi i Punonjësve":
    st.header("👨‍💼 Menaxhimi i Punonjësve")
    st.write("Shto dhe menaxho punonjësit e biznesit tuaj.")
    
    # Krijo DataFrame për punonjësit nëse nuk ekziston
    if 'employees' not in st.session_state:
        st.session_state['employees'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])

    # Form për të shtuar punonjës
    with st.form("add_employee_form"):
        emp_first_name = st.text_input("Emri")
        emp_last_name = st.text_input("Mbiemri")
        emp_position = st.text_input("Pozita")
        emp_phone = st.text_input("Numri i Telefonit")
        emp_email = st.text_input("Email")
        emp_submitted = st.form_submit_button("Shto Punonjësin")

        if emp_submitted:
            new_employee = pd.DataFrame([[emp_first_name, emp_last_name, emp_position, emp_phone, emp_email]], columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])
            st.session_state['employees'] = pd.concat([st.session_state['employees'], new_employee], ignore_index=True)
            st.success(f"Punonjësi '{emp_first_name} {emp_last_name}' u shtua me sukses!")

    # Shfaq tabelën e punonjësve aktual
    st.subheader("Lista e Punonjësve")
    st.dataframe(st.session_state['employees'])
