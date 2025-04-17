import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuration ---
st.set_page_config(page_title="Crêp'Time - Simulateur Business", layout="wide")
st.title("🥞 Crêp'Time - Simulateur de Profit Net")
st.markdown("<h3 style='color:#4682B4'>Estimation des revenus et profits mensuels</h3>", unsafe_allow_html=True)

# --- Sidebar: Paramètres produits ---
st.sidebar.markdown("## 💾 Produits vendus")

def produit_section(nom, emoji):
    st.sidebar.markdown(f"### {emoji} {nom}")
    prix = st.sidebar.number_input(f"Prix unitaire - {nom}", min_value=0, value=30)
    cout = st.sidebar.number_input(f"Coût unitaire - {nom}", min_value=0, value=10)
    commandes = st.sidebar.number_input(f"Commandes/jour - {nom}", min_value=0, value=50)
    return {"prix": prix, "cout": cout, "commandes": commandes}

produits = {
    "Crêpe": produit_section("Crêpe", "🥞"),
    "Gaufre": produit_section("Gaufre", "🧇"),
    "Pancake": produit_section("Pancake", "🥞"),
    "Glace": produit_section("Glace", "🍦"),
    "Salade/Bowl": produit_section("Salade/Bowl", "🥗"),
    "Jus": produit_section("Jus", "🥤"),
    "Boisson chaude": produit_section("Boisson chaude", "☕"),
}

# --- Sidebar: Paramètres globaux ---
st.sidebar.markdown("## ⚙️ Paramètres généraux")
jours = st.sidebar.slider("Jours d'activité/mois", 20, 31, 30)
associes = st.sidebar.number_input("Nombre d’associés", min_value=1, value=2)
taux_impot = st.sidebar.slider("Taux d’impôt (%)", 0, 50, 20) / 100

# --- Sidebar: Charges mensuelles ---
st.sidebar.markdown("## 💸 Charges mensuelles")
loyer = st.sidebar.number_input("Loyer", value=7000)
salaires = st.sidebar.number_input("Salaires employés", value=6000)
elec = st.sidebar.number_input("Électricité", value=4000)
internet = st.sidebar.number_input("Internet", value=300)
menage = st.sidebar.number_input("Femme de ménage", value=1000)
pub = st.sidebar.number_input("Publicité & Réseaux", value=2000)
divers = st.sidebar.number_input("Autres charges", value=1000)

charges_mensuelles = loyer + salaires + elec + internet + menage + pub + divers

# --- Sidebar: Charges d'investissement ---
st.sidebar.markdown("## 🏗️ Charges d’investissement")
equip = st.sidebar.number_input("Équipements", value=50000)
amenagement = st.sidebar.number_input("Aménagement & déco", value=30000)
divers_inv = st.sidebar.number_input("Autres (pubs, 2 mois de loyer...)", value=25000)
charges_invest = equip + amenagement + divers_inv

# --- Calculs principaux ---
revenu_total = sum(p["prix"] * p["commandes"] * jours for p in produits.values())
cout_total = sum(p["cout"] * p["commandes"] * jours for p in produits.values())
benefice_avant_impot = revenu_total - cout_total - charges_mensuelles
impot = max(0, benefice_avant_impot * taux_impot)
profit_net = benefice_avant_impot - impot
part_associe = profit_net / associes

# --- Affichage des résultats ---
st.markdown("### 📊 Résultats Financiers Mensuels")
df_resultats = pd.DataFrame({
    "Indicateur": [
        "Revenu brut",
        "Coût total",
        "Charges mensuelles",
        "Bénéfice avant impôt",
        "Impôt",
        "Profit net",
        "Part par associé"
    ],
    "Valeur (MAD)": [
        revenu_total,
        cout_total,
        charges_mensuelles,
        benefice_avant_impot,
        impot,
        profit_net,
        part_associe
    ]
})
st.dataframe(df_resultats.style.format({"Valeur (MAD)": "{:,.0f}"}), use_container_width=True)

# --- Graphique ---
st.markdown("### 📈 Visualisation du Profit Net")
fig, ax = plt.subplots()
ax.bar(["Revenu", "Coût", "Charges", "Profit Net"], [revenu_total, cout_total, charges_mensuelles, profit_net], color=["#4caf50", "#f44336", "#ff9800", "#2196f3"])
ax.set_ylabel("MAD")
ax.set_title("Comparaison des composantes financières")
st.pyplot(fig)

# --- Charges d’investissement ---
st.markdown("### 💼 Charges d’Investissement")
df_inv = pd.DataFrame({
    "Catégorie": ["Équipements", "Aménagement", "Divers"],
    "Montant (MAD)": [equip, amenagement, divers_inv]
})
df_inv.loc[len(df_inv.index)] = ["TOTAL", charges_invest]
st.dataframe(df_inv.style.format({"Montant (MAD)": "{:,.0f}"}), use_container_width=True)
