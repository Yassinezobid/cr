
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crêp'Time - Simulation Crêpes & Café", layout="wide")
st.title("🥞☕ Crêp'Time - Rentabilité Réelle : Crêpes & Cafés uniquement")

# === Produits : prix, coût ===
st.sidebar.header("🧾 Paramètres Produits")

prix_crepe = st.sidebar.number_input("Prix crêpe (MAD)", value=30)
cout_crepe = st.sidebar.number_input("Coût MP crêpe (MAD)", value=10)

prix_cafe = st.sidebar.number_input("Prix café (MAD)", value=12)
cout_cafe = st.sidebar.number_input("Coût MP café (MAD)", value=3)

# === Quantité de ventes par jour ===
st.sidebar.header("🧮 Ventes quotidiennes")
nbr_crepes = st.sidebar.number_input("Nombre de crêpes vendues par jour", value=30)
nbr_cafes = st.sidebar.number_input("Nombre de cafés vendus par jour", value=40)

# === Marge unitaire ===
marge_crepe = prix_crepe - cout_crepe
marge_cafe = prix_cafe - cout_cafe

st.markdown(f"🥞 Marge nette crêpe : **{marge_crepe:.2f} MAD**")
st.markdown(f"☕ Marge nette café : **{marge_cafe:.2f} MAD**")

# === Paramètres de gestion ===
st.sidebar.header("⚙️ Paramètres de gestion")
jours_mois = st.sidebar.slider("Jours d'activité par mois", 20, 31, 30)
associes = st.sidebar.number_input("Nombre d'associés", value=6)
impot_taux = st.sidebar.slider("Taux impôt (%)", 0, 50, 20) / 100

# === Charges fixes ===
st.sidebar.header("🏗️ Charges Fixes")
local = st.sidebar.number_input("Droit au local", value=100000)
materiel = st.sidebar.number_input("Matériel cuisine", value=50000)
mobilier = st.sidebar.number_input("Mobilier / déco", value=30000)
stock = st.sidebar.number_input("Stock initial", value=10000)
divers_fixes = st.sidebar.number_input("Divers (fixe)", value=10000)
charges_fixes_totales = local + materiel + mobilier + stock + divers_fixes
part_fixe_associe = charges_fixes_totales / associes

# === Charges mensuelles ===
st.sidebar.header("📆 Charges Mensuelles")
loyer = st.sidebar.number_input("Loyer", value=4000)
salaires = st.sidebar.number_input("Salaires employés", value=4000)
menage = st.sidebar.number_input("Femme de ménage", value=1000)
electricite = st.sidebar.number_input("Électricité", value=1500)
internet = st.sidebar.number_input("Internet", value=500)
pub = st.sidebar.number_input("Publicité / Réseaux", value=500)
divers_mensuels = st.sidebar.number_input("Divers", value=1000)
charges_mensuelles = loyer + salaires + menage + electricite + internet + pub + divers_mensuels
part_mensuelle_associe = charges_mensuelles / associes

# === Calculs ===
revenu_net_crepes = marge_crepe * nbr_crepes * jours_mois
revenu_net_cafes = marge_cafe * nbr_cafes * jours_mois
revenu_total = revenu_net_crepes + revenu_net_cafes

benefice_avant_impot = revenu_total - charges_mensuelles
impot = max(0, benefice_avant_impot * impot_taux)
profit_net = benefice_avant_impot - impot
part_associe = profit_net / associes

# === Affichage ===
st.subheader("📊 Résultats")
st.markdown(f"🥞 Revenu net crêpes : **{revenu_net_crepes:,.0f} MAD**")
st.markdown(f"☕ Revenu net cafés : **{revenu_net_cafes:,.0f} MAD**")
st.markdown(f"💵 **Revenu total net : {revenu_total:,.0f} MAD**")
st.markdown(f"📉 Charges mensuelles : {charges_mensuelles:,.0f} MAD")
st.markdown(f"💰 Profit net (après impôt) : **{profit_net:,.0f} MAD**")
st.markdown(f"👥 Part individuelle : **{part_associe:,.0f} MAD**")

# Graphique
st.subheader("📈 Visualisation")
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(["Crêpes", "Cafés"], [revenu_net_crepes, revenu_net_cafes], color=["#f4a261", "#2a9d8f"])
ax.set_ylabel("Revenu net (MAD)")
ax.set_title("Répartition du Revenu Net par Produit")
st.pyplot(fig)

# Charges Résumées
st.subheader("💼 Charges Fixes")
df_fixes = pd.DataFrame({
    "Poste": ["Local", "Matériel", "Mobilier", "Stock", "Divers"],
    "Montant": [local, materiel, mobilier, stock, divers_fixes]
})
df_fixes.loc["Total"] = ["TOTAL", charges_fixes_totales]
st.dataframe(df_fixes)

st.markdown(f"🧾 **Part Fixe Associé : {part_fixe_associe:,.0f} MAD**")

st.subheader("📅 Charges Mensuelles")
df_mensuelles = pd.DataFrame({
    "Poste": ["Loyer", "Salaires", "Ménage", "Électricité", "Internet", "Publicité", "Divers"],
    "Montant": [loyer, salaires, menage, electricite, internet, pub, divers_mensuels]
})
df_mensuelles.loc["Total"] = ["TOTAL", charges_mensuelles]
st.dataframe(df_mensuelles)

st.markdown(f"💸 **Part Mensuelle Associé : {part_mensuelle_associe:,.0f} MAD**")
