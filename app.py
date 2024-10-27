import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Titulli kryesor i aplikacionit
st.set_page_config(page_title="Biznesi Menaxhimi – All in One")
st.title("Biznesi Menaxhimi - All in One")

# Menuja për të zgjedhur seksionin
menu = ["Parashikimi i Shitjeve", "Menaxhimi i Inventarit", "Menaxhimi i Klientëve", "Raportet Financiare", "Menaxhimi i Punonjësve"]
choice = st.sidebar.selectbox("Zgjidh një funksion:", menu)

# Parashikimi i Shitjeve
if choice == "Parashikimi i Shitjeve":
    st.header("🔮 Parashikimi i Shitjeve")
    st.write("Ky seksion ju ndihmon të parashikoni shitjet e ardhshme bazuar në të dhënat ekzistuese.")
    
    # Kodi për parashikimin e shitjeve do të shtohet më vonë

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
    
    # Kodi për menaxhimin e klientëve, për të shtuar, përditësuar dhe fshirë klientë

# Raportet Financiare
elif choice == "Raportet Financiare":
    st.header("💲 Raportet Financiare")
    st.write("Gjenero dhe analizoni raportet financiare të biznesit tuaj.")
    
    # Kodi për raportet financiare për të analizuar të ardhurat dhe shpenzimet mujore

# Menaxhimi i Punonjësve
elif choice == "Menaxhimi i Punonjësve":
    st.header("👨‍💼 Menaxhimi i Punonjësve")
    st.write("Shto dhe menaxho punonjësit e biznesit tuaj.")
    
    # Kodi për menaxhimin e punonjësve, për të shtuar, përditësuar dhe fshirë punonjës
