import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Titulli kryesor i aplikacionit
st.set_page_config(page_title="Biznesi Menaxhimi – All in One")
st.title("Biznesi Menaxhimi - All in One")

# Menuja për të zgjedhur seksionin
menu = [
    "Parashikimi i Shitjeve", 
    "Menaxhimi i Inventarit", 
    "Menaxhimi i Klientëve", 
    "Raportet Financiare", 
    "Menaxhimi i Punonjësve"
]
choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

# Parashikimi i Shitjeve
if choice == "Parashikimi i Shitjeve":
    st.header("🔮 Parashikimi i Shitjeve")
    st.write("Ky seksion ju ndihmon të parashikoni shitjet e ardhshme bazuar në të dhënat ekzistuese.")
    months = st.number_input("Fut numrin e muajit (1-12):", min_value=1, max_value=12, step=1)
    if st.button("Parashiko shitjet"):
        # Ky shembull përdor një model linear të thjeshtë për parashikim (përdorni të dhënat reale për rezultate më të sakta)
        sales = months * 2500 + 5000
        st.success(f"Parashikimi për shitjet është: {sales:.2f} €")
        # Grafiku
        x = list(range(1, months + 1))
        y = [i * 2500 + 5000 for i in x]
        plt.plot(x, y)
        plt.xlabel("Muajt")
        plt.ylabel("Shitjet (€)")
        plt.title("Parashikimi i Shitjeve")
        st.pyplot(plt)

# Menaxhimi i Inventarit
elif choice == "Menaxhimi i Inventarit":
    st.header("📦 Menaxhimi i Inventarit")
    st.write("Shto, menaxho dhe përditëso inventarin e biznesit tuaj.")
    
    # Kontrollo nëse ekziston DataFrame për inventarin në sesionin e Streamlit
    if 'inventory' not in st.session_state:
        st.session_state['inventory'] = pd.DataFrame(columns=["Emri i Produktit", "Kategori", "Sasia", "Çmimi (€)", "Data e Skadencës"])

    # Form për të shtuar artikujt e inventarit
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

    # Tabela e Inventarit
    st.subheader("Inventari Aktual")
    st.dataframe(st.session_state['inventory'])

    # Kontrollo produktet afër skadimit dhe lajmëro përdoruesin
    st.subheader("Produktet Afër Skadimit")
    if 'inventory' in st.session_state:
        expiring_soon = st.session_state['inventory'][
            (st.session_state['inventory']["Data e Skadencës"].notnull()) &
            (st.session_state['inventory']["Data e Skadencës"] <= datetime.now() + timedelta(days=7))
        ]
        if not expiring_soon.empty:
            st.warning("Këto produkte do të skadojnë së shpejti:")
            st.dataframe(expiring_soon)
        else:
            st.info("Asnjë produkt nuk është afër skadimit.")

# Menaxhimi i Klientëve
elif choice == "Menaxhimi i Klientëve":
    st.header("👥 Menaxhimi i Klientëve")
    st.write("Mbaj shënim informacionet e klientëve tuaj.")
    
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
    
    st.subheader("Lista e Klientëve")
    st.dataframe(st.session_state['clients'])

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💲 Raportet Financiare")
    st.write("Gjenero dhe analizoni raportet financiare të biznesit tuaj.")
    
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
        
        # Shembull i një grafiku për të treguar të ardhurat dhe shpenzimet mujore
        months = ["Janar", "Shkurt", "Mars", "Prill", "Maj", "Qershor", "Korrik", "Gusht", "Shtator", "Tetor", "Nëntor", "Dhjetor"]
        monthly_profit = [profit for _ in range(12)]
        plt.plot(months, monthly_profit, marker='o')
        plt.xlabel("Muajt")
        plt.ylabel("Fitimi (€)")
        plt.title("Fitimi Mujor gjatë Vitit")
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
        add_employee = st.form_submit_button("Shto Punonjësin")
        
        if add_employee:
            employee_data = pd.DataFrame([[employee_name, employee_surname, employee_position, employee_phone, employee_email]], 
                                         columns=["Emri", "Mbiemri", "Pozita", "Numri i Telefonit", "Email"])
            st.session_state['employees'] = pd.concat([st.session_state['employees'], employee_data], ignore_index=True)
            st.success(f"Punonjësi '{employee_name} {employee_surname}' u shtua me sukses!")
    
    st.subheader("Lista e Punonjësve")
    st.dataframe(st.session_state['employees'])
