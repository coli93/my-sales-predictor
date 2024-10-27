import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Titulli kryesor i aplikacionit
st.set_page_config(page_title="Biznesi Menaxhimi - All in One")
st.title("Biznesi Menaxhimi - All in One")

# Menuja për të zgjedhur seksionin
menu = ["Parashikimi i Shitjeve", "Menaxhimi i Inventarit", "Menaxhimi i Klientëve", "Raportet Financiare", "Menaxhimi i Punonjësve"]
choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

# Parashikimi i Shitjeve
if choice == "Parashikimi i Shitjeve":
    st.header("🔮 Parashikimi i Shitjeve")
    st.write("Ky seksion ju ndihmon të parashikoni shitjet mujore bazuar në të dhënat ekzistuese.")
    
    # Shto logjikën për parashikimin e shitjeve
    month = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)
    if st.button("Parashiko shitjet"):
        predicted_sales = month * 2500  # Vendos një formulë të thjeshtë për shembull
        st.write(f"Parashikimi për shitjet është: {predicted_sales:.2f}")
        # Grafiku
        months = list(range(1, 13))
        sales = [m * 2500 for m in months]
        plt.plot(months, sales)
        plt.xlabel("Muajt")
        plt.ylabel("Shitjet (€)")
        plt.title("Parashikimi i Shitjeve për Bizneset")
        st.pyplot(plt)

# Menaxhimi i Inventarit
elif choice == "Menaxhimi i Inventarit":
    st.header("📦 Menaxhimi i Inventarit")
    st.write("Shto, menaxho dhe përditëso inventarin e biznesit tuaj.")
    
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=['Emri', 'Sasia', 'Çmimi', 'Kategoria', 'Skadenca'])

    # Form për të shtuar artikuj
    with st.form("add_item_form"):
        item_name = st.text_input("Emri i Artikullit")
        item_qty = st.number_input("Sasia", min_value=0, step=1)
        item_price = st.number_input("Çmimi (€)", min_value=0.0, step=0.01)
        item_category = st.text_input("Kategoria")
        item_expiry = st.date_input("Data e Skadencës (opsionale)", value=None)
        submitted = st.form_submit_button("Shto Artikullin")

        if submitted:
            new_data = pd.DataFrame([[item_name, item_qty, item_price, item_category, item_expiry]], 
                                    columns=['Emri', 'Sasia', 'Çmimi', 'Kategoria', 'Skadenca'])
            st.session_state['inventory'] = pd.concat([st.session_state['inventory'], new_data], ignore_index=True)
            st.success(f"Artikulli '{item_name}' u shtua në inventar!")

    # Shfaq tabelën e inventarit aktual
    st.subheader("Inventari Aktual")
    st.dataframe(st.session_state['inventory'])

    # Kontrollo produktet afër skadimit
    st.subheader("Produktet Afër Skadimit")
    current_date = datetime.now().date()
    near_expiry = st.session_state['inventory'][st.session_state['inventory']['Skadenca'].apply(lambda x: x <= current_date if pd.notna(x) else False)]

    if not near_expiry.empty:
        st.warning("Produkte afër skadimit ose të skaduara:")
        st.write(near_expiry)
    else:
        st.success("Nuk ka produkte afër skadimit.")

# Menaxhimi i Klientëve
elif choice == "Menaxhimi i Klientëve":
    st.header("👥 Menaxhimi i Klientëve")
    st.write("Mbaj shënim informacionet e klientëve tuaj.")
    
    if 'clients' not in st.session_state:
        st.session_state['clients'] = pd.DataFrame(columns=['Emri', 'Mbiemri', 'Email', 'Numri i Telefonit'])

    # Form për të shtuar klientë
    with st.form("add_client_form"):
        client_name = st.text_input("Emri")
        client_surname = st.text_input("Mbiemri")
        client_email = st.text_input("Email")
        client_phone = st.text_input("Numri i Telefonit")
        submitted = st.form_submit_button("Shto Klientin")

        if submitted:
            new_client = pd.DataFrame([[client_name, client_surname, client_email, client_phone]], 
                                      columns=['Emri', 'Mbiemri', 'Email', 'Numri i Telefonit'])
            st.session_state['clients'] = pd.concat([st.session_state['clients'], new_client], ignore_index=True)
            st.success(f"Klienti '{client_name} {client_surname}' u shtua me sukses!")

    # Shfaq listën e klientëve
    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💰 Raportet Financiare")
    st.write("Gjenero dhe analizo raportet financiare të biznesit tuaj.")
    
    # Form për të gjeneruar raportin financiar
    revenue = st.number_input("Të ardhurat mujore (€)", min_value=0.0, step=0.01)
    expenses = st.number_input("Shpenzimet mujore (€)", min_value=0.0, step=0.01)
    if st.button("Gjenero Raportin"):
        profit = revenue - expenses
        st.write(f"Të ardhurat mujore: €{revenue:.2f}")
        st.write(f"Shpenzimet mujore: €{expenses:.2f}")
        st.write(f"Fitimi: €{profit:.2f}")
        if profit < 0:
            st.error("Biznesi është në humbje!")
        else:
            st.success("Biznesi është në fitim!")
        
        # Grafiku për të ardhurat
        months = ['Janar', 'Shkurt', 'Mars', 'Prill', 'Maj', 'Qershor', 'Korrik', 'Gusht', 'Shtator', 'Tetor', 'Nëntor', 'Dhjetor']
        monthly_profits = [profit] * 12
        plt.figure(figsize=(10, 5))
        plt.plot(months, monthly_profits, marker='o')
        plt.xlabel("Muajt")
        plt.ylabel("Fitimi (€)")
        plt.title("Fitimi Mujor gjatë Vitit")
        st.pyplot(plt)

# Menaxhimi i Punonjësve
elif choice == "Menaxhimi i Punonjësve":
    st.header("👨‍💼 Menaxhimi i Punonjësve")
    st.write("Shto dhe menaxho punonjësit e biznesit tuaj.")
    
    if 'employees' not in st.session_state:
        st.session_state['employees'] = pd.DataFrame(columns=['Emri', 'Mbiemri', 'Pozita', 'Numri i Telefonit', 'Email'])

    # Form për të shtuar punonjës
    with st.form("add_employee_form"):
        employee_name = st.text_input("Emri")
        employee_surname = st.text_input("Mbiemri")
        employee_position = st.text_input("Pozita")
        employee_phone = st.text_input("Numri i Telefonit")
        employee_email = st.text_input("Email")
        submitted = st.form_submit_button("Shto Punonjësin")

        if submitted:
            new_employee = pd.DataFrame([[employee_name, employee_surname, employee_position, employee_phone, employee_email]], 
                                        columns=['Emri', 'Mbiemri', 'Pozita', 'Numri i Telefonit', 'Email'])
            st.session_state['employees'] = pd.concat([st.session_state['employees'], new_employee], ignore_index=True)
            st.success(f"Punonjësi '{employee_name} {employee_surname}' u shtua me sukses!")

    # Shfaq listën e punonjësve
    st.subheader("Lista e Punonjësve")
    st.dataframe(st.session_state['employees'])
