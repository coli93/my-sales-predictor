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
    
    # Shto logjikë për menaxhimin e klientëve këtu...

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💰 Raportet Financiare")
    st.write("Gjenero dhe analizoni raportet financiare të biznesit tuaj.")
    
    # Shto logjikë për raportet financiare këtu...

# Menaxhimi i Punonjësve
elif choice == "Menaxhimi i Punonjësve":
    st.header("👷‍♀️ Menaxhimi i Punonjësve")
    st.write("Shto dhe menaxho punonjësit e biznesit tuaj.")
    
    # Shto logjikë për menaxhimin e punonjësve këtu...
