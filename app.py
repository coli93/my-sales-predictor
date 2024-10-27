import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Konfigurimi i aplikacionit
st.set_page_config(page_title="Biznesi Menaxhimi – All in One")

# Titulli kryesor
st.title("Biznesi Menaxhimi – All in One")

# Menuja për të zgjedhur seksionin
menu = ["Parashikimi i Shitjeve", "Menaxhimi i Inventarit", "Menaxhimi i Klientëve", "Raportet Financiare", "Menaxhimi i Punonjësve", "Produktet Afër Skadimit"]
choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

# Parashikimi i Shitjeve
if choice == "Parashikimi i Shitjeve":
    st.header("🔮 Parashikimi i Shitjeve")
    st.write("Ky seksion ju ndihmon të parashikoni shitjet mujore për bizneset bazuar në të dhënat ekzistuese.")
    # Logjika për parashikimin e shitjeve mund të shtohet këtu

# Menaxhimi i Inventarit
elif choice == "Menaxhimi i Inventarit":
    st.header("📦 Menaxhimi i Inventarit")
    st.write("Shto, menaxho dhe përditëso inventarin e biznesit tuaj.")

    # Kontrollo gjendjen e inventarit në session_state
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Emri", "Sasia", "Çmimi", "Data Skadimit", "Kategoria"])

    # Form për të shtuar artikuj
    with st.form("add_item_form"):
        item_name = st.text_input("Emri i Artikullit")
        item_qty = st.number_input("Sasia", min_value=0)
        item_price = st.number_input("Çmimi (€)", min_value=0.0, format="%.2f")
        item_expiry = st.date_input("Data e Skadimit (Opsionale)")
        item_category = st.text_input("Kategoria")
        submitted = st.form_submit_button("Shto Artikullin")

        if submitted:
            new_data = pd.DataFrame([[item_name, item_qty, item_price, item_expiry, item_category]],
                                    columns=["Emri", "Sasia", "Çmimi", "Data Skadimit", "Kategoria"])
            st.session_state['inventory'] = pd.concat([st.session_state['inventory'], new_data], ignore_index=True)
            st.success(f"Artikulli '{item_name}' u shtua në inventar!")

    # Shfaq tabelën e inventarit aktual
    st.subheader("Inventari Aktual")
    if not st.session_state['inventory'].empty:
        for idx, row in st.session_state['inventory'].iterrows():
            with st.expander(f"{row['Emri']} - {row['Kategoria']}"):
                st.write(f"Sasia për {row['Emri']}: {row['Sasia']}")
                st.write(f"Çmimi për {row['Emri']} (€): {row['Çmimi']}")
                st.write(f"Data Skadimit: {row['Data Skadimit'] if pd.notnull(row['Data Skadimit']) else 'Pa skadencë'}")
                update_qty = st.number_input(f"Sasia për {row['Emri']}", value=row['Sasia'])
                update_price = st.number_input(f"Çmimi për {row['Emri']} (€)", value=row['Çmimi'], format="%.2f")
                delete_button = st.button(f"Fshij {row['Emri']}")
                update_button = st.button(f"Përditëso {row['Emri']}")

                if delete_button:
                    st.session_state['inventory'].drop(index=idx, inplace=True)
                    st.success(f"Artikulli '{row['Emri']}' u fshi nga inventari.")
                if update_button:
                    st.session_state['inventory'].at[idx, 'Sasia'] = update_qty
                    st.session_state['inventory'].at[idx, 'Çmimi'] = update_price
                    st.success(f"Artikulli '{row['Emri']}' u përditësua.")

# Menaxhimi i Klientëve
elif choice == "Menaxhimi i Klientëve":
    st.header("🧑‍🤝‍🧑 Menaxhimi i Klientëve")
    st.write("Mbaj shënim informacionet e klientëve dhe menaxho kontaktet e tyre.")

    if 'clients' not in st.session_state:
        st.session_state['clients'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])

    with st.form("add_client_form"):
        client_name = st.text_input("Emri")
        client_surname = st.text_input("Mbiemri")
        client_email = st.text_input("Email")
        client_phone = st.text_input("Numri i Telefonit")
        client_submitted = st.form_submit_button("Shto Klientin")

        if client_submitted:
            new_client = pd.DataFrame([[client_name, client_surname, client_email, client_phone]],
                                      columns=["Emri", "Mbiemri", "Email", "Numri i Telefonit"])
            st.session_state['clients'] = pd.concat([st.session_state['clients'], new_client], ignore_index=True)
            st.success(f"Klienti '{client_name} {client_surname}' u shtua me sukses!")

    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💲 Raportet Financiare")
    st.write("Gjenero dhe analizoni raportet financiare të biznesit tuaj.")

    income = st.number_input("Të ardhurat mujore (€)", min_value=0.0, format="%.2f")
    expense = st.number_input("Shpenzimet mujore (€)", min_value=0.0, format="%.2f")
    generate_report = st.button("Gjenero Raportin")

    if generate_report:
        profit = income - expense
        st.subheader("Raporti Financiar")
        st.write(f"Të ardhurat mujore: €{income:.2f}")
        st.write(f"Shpenzimet mujore: €{expense:.2f}")
        st.write(f"Fitimi: €{profit:.2f}")
        if profit > 0:
            st.success("Biznesi është në fitim!")
        else:
            st.warning("Biznesi është në humbje!")

        # Grafiku i fitimeve mujore për ilustrim
        months = ["Janar", "Shkurt", "Mars", "Prill", "Maj", "Qershor", "Korrik", "Gusht", "Shtator", "Tetor", "Nëntor", "Dhjetor"]
        profits = [profit] * 12  # Simulim për ilustrim
        plt.plot(months, profits, marker='o')
        plt.title("Fitimi Mujor gjatë Vitit")
        plt.xlabel("Muajt")
        plt.ylabel("Fitimi (€)")
        plt.grid(True)
        st.pyplot(plt)

# Menaxhimi i Punonjësve
elif choice == "Menaxhimi i Punonjësve":
    st.header("👨‍💼 Menaxhimi i Punonjësve")
    st.write("Shto dhe menaxho punonjësit e biznesit tuaj.")

    if 'employees' not in st.session_state:
        st.session_state['employees'] = pd.DataFrame(columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])

    with st.form("add_employee_form"):
        employee_name = st.text_input("Emri")
        employee_surname = st.text_input("Mbiemri")
        employee_position = st.text_input("Pozita")
        employee_phone = st.text_input("Numri i Telefonit")
        employee_email = st.text_input("Email")
        employee_submitted = st.form_submit_button("Shto Punonjësin")

        if employee_submitted:
            new_employee = pd.DataFrame([[employee_name, employee_surname, employee_position, employee_phone, employee_email]],
                                        columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])
            st.session_state['employees'] = pd.concat([st.session_state['employees'], new_employee], ignore_index=True)
            st.success(f"Punonjësi '{employee_name} {employee_surname}' u shtua me sukses!")

    st.subheader("Lista e Punonjësve")
    st.dataframe(st.session_state['employees'])

# Produktet Afër Skadimit
elif choice == "Produktet Afër Skadimit":
    st.header("📅 Produktet Afër Skadimit")
    if 'inventory' in st.session_state:
        today = pd.to_datetime(datetime.now().date())
        products_expiring = st.session_state['inventory'][st.session_state['inventory']['Data Skadimit'].apply(lambda x: pd.notnull(x) and x <= (today + timedelta(days=30)))]
        if not products_expiring.empty:
            st.warning("Produkte që skadojnë brenda muajit:")
            st.dataframe(products_expiring)
        else:
            st.success("Nuk ka produkte afër skadimit!")
