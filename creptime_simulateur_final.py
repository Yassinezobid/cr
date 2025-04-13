
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crêp'Time - Simulateur Complet", layout="wide")
st.title("🥞 Simulateur de Rentabilité - Crêp'Time (Meknès)")

# === Produits : prix, coût, consommation ===
st.sidebar.header("🧾 Paramètres Produits & Marges")

# Crêpes
st.sidebar.markdown("### 🧁 Crêpes")
prix_crepe = st.sidebar.number_input("Prix crêpe (MAD)", value=30)
cout_crepe = st.sidebar.number_input("Coût crêpe (MP)", value=10)

# Jus / Smoothies
st.sidebar.markdown("### 🍹 Jus / Smoothies")
prix_jus = st.sidebar.number_input("Prix jus (MAD)", value=20)
cout_jus = st.sidebar.number_input("Coût jus (MP)", value=7)

# Café
st.sidebar.markdown("### ☕ Café")
prix_cafe = st.sidebar.number_input("Prix café (MAD)", value=12)
cout_cafe = st.sidebar.number_input("Coût café (MP)", value=3)

# Glace
st.sidebar.markdown("### 🍨 Glace")
prix_glace = st.sidebar.number_input("Prix glace (MAD)", value=15)
cout_glace = st.sidebar.number_input("Coût glace (MP)", value=5)

# Calcul marge nette/client
marge_crepe = prix_crepe - cout_crepe
marge_jus = prix_jus - cout_jus
marge_cafe = prix_cafe - cout_cafe
marge_glace = prix_glace - cout_glace
panier_moyen = marge_crepe + marge_jus + marge_cafe + marge_glace

st.markdown(f"🧺 **Panier moyen net par client : {panier_moyen:.2f} MAD**")

# === Paramètres de gestion ===
st.sidebar.header("⚙️ Paramètres de gestion")
clients_min = st.sidebar.slider("Clients/jour (min)", 5, 50, 15)
clients_max = st.sidebar.slider("Clients/jour (max)", 50, 200, 80)
pas = st.sidebar.slider("Pas variation", 1, 10, 5)
jours_mois = st.sidebar.slider("Jours d'activité par mois", 20, 31, 30)
associes = st.sidebar.number_input("Nombre d'associés", value=6)
impot_taux = st.sidebar.slider("Taux impôt (%)", 0, 50, 20) / 100

# === Charges fixes détaillées ===
st.sidebar.header("🏗️ Charges Fixes (Investissement)")
local = st.sidebar.number_input("Droit au local", value=100000)
travaux = st.sidebar.number_input("Travaux / déco", value=25000)
materiel = st.sidebar.number_input("Matériel cuisine", value=50000)
mobilier = st.sidebar.number_input("Mobilier", value=20000)
ambiance = st.sidebar.number_input("Ambiance / TV / déco", value=15000)
stock = st.sidebar.number_input("Stock initial", value=10000)
divers_fixes = st.sidebar.number_input("Divers (fixe)", value=10000)

charges_fixes_totales = sum([local, travaux, materiel, mobilier, ambiance, stock, divers_fixes])
part_fixe_associe = charges_fixes_totales / associes

# === Charges mensuelles détaillées ===
st.sidebar.header("📆 Charges Mensuelles")
loyer = st.sidebar.number_input("Loyer", value=4000)
salaire_employes = st.sidebar.number_input("Salaires employés (2)", value=4000)
salaire_menage = st.sidebar.number_input("Femme de ménage", value=1000)
electricite = st.sidebar.number_input("Électricité", value=1500)
internet = st.sidebar.number_input("Internet", value=500)
publicite = st.sidebar.number_input("Publicité / Réseaux", value=500)
divers_mensuels = st.sidebar.number_input("Divers mensuels", value=1000)

charges_mensuelles = sum([
    loyer, salaire_employes, salaire_menage,
    electricite, internet, publicite, divers_mensuels
])
part_mensuelle_associe = charges_mensuelles / associes

# === Simulation ===
clients_range = list(range(clients_min, clients_max + 1, pas))
data = []

for clients in clients_range:
    revenu_brut = clients * panier_moyen * jours_mois
    benefice_avant_impot = revenu_brut - charges_mensuelles
    impot = max(0, benefice_avant_impot * impot_taux)
    profit_net = benefice_avant_impot - impot
    part_associe = profit_net / associes
    data.append([
        clients, panier_moyen, revenu_brut, benefice_avant_impot,
        impot, profit_net, part_associe
    ])

df = pd.DataFrame(data, columns=[
    "Clients/Jour", "Panier Moyen Net", "Revenu Brut",
    "Bénéfice Avant Impôt", "Impôt", "Profit Net", "Part par Associé"
])

# === Affichage ===
st.subheader("📊 Résultats de Simulation")
st.dataframe(df.style.format("{:,.0f}"))

st.subheader("📈 Graphique : Profit Net & Part Associé")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Clients/Jour"], df["Profit Net"], color='orange', label="Profit Net")
ax.plot(df["Clients/Jour"], df["Part par Associé"], marker='o', color='green', label="Part par Associé")
ax.set_title("Profit Net mensuel selon la fréquentation")
ax.set_xlabel("Clients par jour")
ax.set_ylabel("MAD")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# === Résumé des Charges ===
st.subheader("💼 Charges Fixes")
df_fixes = pd.DataFrame({
    "Poste": ["Local", "Travaux", "Cuisine", "Mobilier", "Ambiance", "Stock", "Divers"],
    "Montant": [local, travaux, materiel, mobilier, ambiance, stock, divers_fixes]
})
df_fixes.loc["Total"] = ["TOTAL", charges_fixes_totales]
st.dataframe(df_fixes)

st.markdown(f"💰 **Part Fixe Associé : {part_fixe_associe:,.0f} MAD**")

st.subheader("📅 Charges Mensuelles")
df_mensuelles = pd.DataFrame({
    "Poste": ["Loyer", "Salaires", "Ménage", "Électricité", "Internet", "Publicité", "Divers"],
    "Montant": [loyer, salaire_employes, salaire_menage, electricite, internet, publicite, divers_mensuels]
})
df_mensuelles.loc["Total"] = ["TOTAL", charges_mensuelles]
st.dataframe(df_mensuelles)

st.markdown(f"💸 **Part Mensuelle Associé : {part_mensuelle_associe:,.0f} MAD**")
