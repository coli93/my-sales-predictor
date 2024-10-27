import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Përcakto konfigurimin e faqes vetëm një herë
st.set_page_config(page_title="Biznesi Menaxhimi - All in One", layout="centered")

# Shto një stil të personalizuar për të rregulluar pamjen e aplikacionit
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

# Titulli kryesor i aplikacionit
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

# Menaxhimi i Inventarit
if choice == "Menaxhimi i Inventarit":
    st.header("📦 Menaxhimi i Inventarit")
    st.write("Shto, menaxho dhe përditëso inventarin e biznesit tuaj.")
    
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

    # Mundësia për të fshirë artikuj nga inventari
    st.subheader("Inventari Aktual")
    inventory_df = st.session_state['inventory']
    st.dataframe(inventory_df)

    if not inventory_df.empty:
        selected_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(inventory_df) - 1, step=1)
        if st.button("Fshi Artikullin"):
            st.session_state['inventory'].drop(index=selected_index, inplace=True)
            st.session_state['inventory'].reset_index(drop=True, inplace=True)
            st.success("Artikulli u fshi me sukses!")

    # Përditësimi i artikujve
    st.subheader("Përditëso Artikullin")
    if not inventory_df.empty:
        update_index = st.selectbox("Zgjidh artikullin për përditësim:", inventory_df.index)
        with st.form("update_item_form"):
            updated_name = st.text_input("Emri i Produktit", inventory_df.at[update_index, "Emri i Produktit"])
            updated_category = st.selectbox("Kategoria", ["Ushqim", "Pije", "Të Tjera"], index=["Ushqim", "Pije", "Të Tjera"].index(inventory_df.at[update_index, "Kategori"]))
            updated_qty = st.number_input("Sasia", min_value=1, step=1, value=inventory_df.at[update_index, "Sasia"])
            updated_price = st.number_input("Çmimi (€)", min_value=0.01, step=0.01, value=inventory_df.at[update_index, "Çmimi (€)"])
            updated_expiry = st.date_input("Data e Skadencës (Opsionale)", value=inventory_df.at[update_index, "Data e Skadencës"] if pd.notnull(inventory_df.at[update_index, "Data e Skadencës"]) else None)
            update_btn = st.form_submit_button("Përditëso Artikullin")
            
            if update_btn:
                st.session_state['inventory'].at[update_index, "Emri i Produktit"] = updated_name
                st.session_state['inventory'].at[update_index, "Kategori"] = updated_category
                st.session_state['inventory'].at[update_index, "Sasia"] = updated_qty
                st.session_state['inventory'].at[update_index, "Çmimi (€)"] = updated_price
                st.session_state['inventory'].at[update_index, "Data e Skadencës"] = updated_expiry
                st.success(f"Artikulli '{updated_name}' u përditësua me sukses!")

    # Kontrollo produktet afër skadimit dhe lajmëro përdoruesin
    st.subheader("Produktet Afër Skadimit")
    try:
        expiring_soon = st.session_state['inventory'][
            (st.session_state['inventory']["Data e Skadencës"].notnull()) &
            (st.session_state['inventory']["Data e Skadencës"] <= datetime.now() + timedelta(days=7))
        ]
        if not expiring_soon.empty:
            st.warning("Këto produkte do të skadojnë së shpejti:")
            st.dataframe(expiring_soon)
        else:
            st.info("Asnjë produkt nuk është afër skadimit.")
    except Exception as e:
        st.error(f"Gabim gjatë përpunimit të skadencave: {e}")
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
    clients_df = st.session_state['clients']
    st.dataframe(clients_df)

    if not clients_df.empty:
        client_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(clients_df) - 1, step=1)
        if st.button("Fshi Klientin"):
            st.session_state['clients'].drop(index=client_index, inplace=True)
            st.session_state['clients'].reset_index(drop=True, inplace=True)
            st.success("Klienti u fshi me sukses!")

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
    employees_df = st.session_state['employees']
    st.dataframe(employees_df)

    if not employees_df.empty:
        employee_index = st.number_input("Indeksi për të fshirë:", min_value=0, max_value=len(employees_df) - 1, step=1)
        if st.button("Fshi Punonjësin"):
            st.session_state['employees'].drop(index=employee_index, inplace=True)
            st.session_state['employees'].reset_index(drop=True, inplace=True)
            st.success("Punonjësi u fshi me sukses!")
