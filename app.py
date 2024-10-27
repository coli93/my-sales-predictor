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
    
    # Shto logjikë për menaxhimin e inventarit këtu...

# Menaxhimi i Klientëve
elif choice == "Menaxhimi i Klientëve":
    st.header("🧑‍🤝‍🧑 Menaxhimi i Klientëve")
    st.write("Mbaj shënim informacionet e klientëve dhe menaxho marrëdhëniet me ta.")
    
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
