
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crêp'Time - Rentabilité Crêpes & Café", layout="wide")
st.title("🥞☕ Crêp'Time - Simulateur de Rentabilité : Crêpes & Cafés")

# === Produits : prix, coût unitaire ===
st.sidebar.header("🧾 Produits")
prix_crepe = st.sidebar.number_input("Prix crêpe (MAD)", value=30)
cout_crepe = st.sidebar.number_input("Coût MP crêpe (MAD)", value=10)

prix_cafe = st.sidebar.number_input("Prix café (MAD)", value=12)
cout_cafe = st.sidebar.number_input("Coût MP café (MAD)", value=3)

# === Quantité par jour ===
st.sidebar.header("🥡 Nombre de ventes par jour")
nbr_crepes_jour = st.sidebar.number_input("Nombre de crêpes par jour", value=60)
nbr_cafes_jour = st.sidebar.number_input("Nombre de cafés par jour", value=40)

# === Paramètres de simulation ===
st.sidebar.header("📊 Simulation")
jours_mois = st.sidebar.slider("Jours/mois", 20, 31, 30)
associes = st.sidebar.number_input("Nombre d'associés", value=6)
impot_taux = st.sidebar.slider("Taux d'imposition (%)", 0, 50, 20) / 100

# === Charges mensuelles ===
st.sidebar.header("📆 Charges Mensuelles")
loyer = st.sidebar.number_input("Loyer", value=10000)
salaires = st.sidebar.number_input("Salaires employés (2)", value=4000)
menage = st.sidebar.number_input("Femme de ménage", value=1000)
electricite = st.sidebar.number_input("Électricité", value=1500)
internet = st.sidebar.number_input("Internet", value=500)
publicite = st.sidebar.number_input("Publicité / Réseaux", value=500)

charges_mensuelles = loyer + salaires + menage + electricite + internet + publicite
part_mensuelle_associe = charges_mensuelles / associes

# === Charges fixes ===
st.sidebar.header("🏗️ Charges Fixes")
invest_initial = st.sidebar.number_input("Investissement initial total (MAD)", value=30000)
part_fixe_associe = invest_initial / associes

# === Simulation : de 10 à 200 unités/jour cumulés ===
st.sidebar.header("🔁 Plage de simulation")
unit_min = st.sidebar.slider("Total unités/jour min", 10, 100, 20)
unit_max = st.sidebar.slider("Total unités/jour max", 100, 200, 100)
pas = st.sidebar.slider("Pas de variation", 1, 20, 10)

# === Marges unitaires ===
marge_crepe = prix_crepe - cout_crepe
marge_cafe = prix_cafe - cout_cafe

# === Simulation dynamique ===
data = []
for total_units in range(unit_min, unit_max + 1, pas):
    ratio_crepe = nbr_crepes_jour / (nbr_crepes_jour + nbr_cafes_jour)
    ratio_cafe = nbr_cafes_jour / (nbr_crepes_jour + nbr_cafes_jour)
    units_crepe = total_units * ratio_crepe
    units_cafe = total_units * ratio_cafe

    panier_moyen = (units_crepe * marge_crepe + units_cafe * marge_cafe) / total_units
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
    "Total unités/jour", "Panier Moyen Net", "Revenu Brut",
    "Bénéfice Avant Impôt", "Impôt", "Profit Net", "Part par Associé"
])

# === Affichage ===
st.markdown(f"🧺 Panier moyen net par unité estimé : **{df['Panier Moyen Net'].iloc[0]:.2f} à {df['Panier Moyen Net'].iloc[-1]:.2f} MAD**")

st.subheader("📊 Évolution du Profit Net")
st.dataframe(df.style.format("{:,.0f}"))

st.subheader("📈 Graphique : Profit Net & Part Associé")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Total unités/jour"], df["Profit Net"], color='orange', label="Profit Net")
ax.plot(df["Total unités/jour"], df["Part par Associé"], marker='o', color='green', label="Part Associé")
ax.set_title("Évolution du Profit Net mensuel (Crêpes + Cafés)")
ax.set_xlabel("Total Unités (Crêpes + Cafés) par jour")
ax.set_ylabel("MAD")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# === Résumé final ===
st.subheader("🧾 Résumé des Charges & Parts")
st.markdown(f"🏗️ **Investissement initial :** {invest_initial:,.0f} MAD")
st.markdown(f"📆 **Charges mensuelles :** {charges_mensuelles:,.0f} MAD")
st.markdown(f"👥 **Part fixe associée :** {part_fixe_associe:,.0f} MAD")
st.markdown(f"💸 **Part mensuelle associée :** {part_mensuelle_associe:,.0f} MAD")
