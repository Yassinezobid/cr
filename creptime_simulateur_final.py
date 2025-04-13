
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crêp'Time - Simulation Crêpes & Café", layout="wide")
st.title("🥞☕ Crêp'Time - Rentabilité Évolutive : Crêpes & Cafés")

# === Produits ===
st.sidebar.header("🧾 Produits & Marges")
prix_crepe = st.sidebar.number_input("Prix crêpe (MAD)", value=30)
cout_crepe = st.sidebar.number_input("Coût MP crêpe (MAD)", value=10)
prix_cafe = st.sidebar.number_input("Prix café (MAD)", value=12)
cout_cafe = st.sidebar.number_input("Coût MP café (MAD)", value=3)

# === Répartition du panier ===
st.sidebar.header("🥡 Répartition Panier Moyen")
pourcentage_crepes = st.sidebar.slider("Pourcentage crêpes dans le panier", 0, 100, 60)
pourcentage_cafes = 100 - pourcentage_crepes

st.sidebar.markdown(f"🔁 {pourcentage_crepes}% Crêpes / {pourcentage_cafes}% Cafés")

# === Paramètres de simulation ===
st.sidebar.header("📊 Simulation")
unit_min = st.sidebar.slider("Unités/jour (min)", 10, 100, 20)
unit_max = st.sidebar.slider("Unités/jour (max)", 100, 200, 100)
pas = st.sidebar.slider("Pas de variation", 1, 20, 10)
jours_mois = st.sidebar.slider("Jours d'activité", 20, 31, 30)
associes = st.sidebar.number_input("Nombre d'associés", value=6)
impot_taux = st.sidebar.slider("Taux impôt (%)", 0, 50, 20) / 100

# === Charges ===
st.sidebar.header("📦 Charges Mensuelles")
charges_mensuelles = st.sidebar.number_input("Charges mensuelles globales (MAD)", value=11500)

# === Charges fixes ===
st.sidebar.header("🏗️ Charges Fixes")
charges_fixes = st.sidebar.number_input("Investissement initial total (MAD)", value=160000)

part_fixe_associe = charges_fixes / associes
part_mensuelle_associe = charges_mensuelles / associes

# === Calcul marges ===
marge_crepe = prix_crepe - cout_crepe
marge_cafe = prix_cafe - cout_cafe

# === Simulation dynamique ===
data = []
for total_units in range(unit_min, unit_max + 1, pas):
    nbr_crepes = total_units * (pourcentage_crepes / 100)
    nbr_cafes = total_units * (pourcentage_cafes / 100)
    panier_moyen = (nbr_crepes * marge_crepe + nbr_cafes * marge_cafe) / total_units

    revenu_brut = panier_moyen * total_units * jours_mois
    benefice_avant_impot = revenu_brut - charges_mensuelles
    impot = max(0, benefice_avant_impot * impot_taux)
    profit_net = benefice_avant_impot - impot
    part_associe = profit_net / associes

    data.append([
        total_units, panier_moyen, revenu_brut,
        benefice_avant_impot, impot, profit_net, part_associe
    ])

df = pd.DataFrame(data, columns=[
    "Unités/Jour", "Panier Moyen Net", "Revenu Brut",
    "Bénéfice Avant Impôt", "Impôt", "Profit Net", "Part par Associé"
])

# === Affichage ===
st.markdown(f"🧺 **Panier moyen net estimé (variable) : {df['Panier Moyen Net'].iloc[0]:.2f} - {df['Panier Moyen Net'].iloc[-1]:.2f} MAD**")

st.subheader("📊 Tableau d'Évolution des Profits")
st.dataframe(df.style.format("{:,.0f}"))

st.subheader("📈 Graphique : Profit Net & Part Associé")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Unités/Jour"], df["Profit Net"], color='orange', label="Profit Net")
ax.plot(df["Unités/Jour"], df["Part par Associé"], marker='o', color='green', label="Part Associé")
ax.set_title("Évolution du Profit Net en fonction des ventes")
ax.set_xlabel("Nombre d'unités (Crêpes + Cafés) / jour")
ax.set_ylabel("MAD")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# === Résumé ===
st.subheader("🧾 Résumé des Charges")
st.markdown(f"🏗️ **Charges fixes totales** : {charges_fixes:,.0f} MAD")
st.markdown(f"📆 **Charges mensuelles** : {charges_mensuelles:,.0f} MAD")
st.markdown(f"👥 **Part fixe associée** : {part_fixe_associe:,.0f} MAD")
st.markdown(f"💸 **Part mensuelle associée** : {part_mensuelle_associe:,.0f} MAD")
