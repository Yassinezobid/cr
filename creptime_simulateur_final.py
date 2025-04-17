import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="📊 Simulateur Business Plan Mensuel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal stylé
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>📊 Simulateur de Business Plan Mensuel</h1>",
    unsafe_allow_html=True
)

# --- SIDEBAR ---
st.sidebar.header("🛠️ Paramètres généraux")
# Jours d'activité par mois
jours_par_mois = st.sidebar.number_input(
    "Nombre de jours d'activité par mois", min_value=1, max_value=31, value=30, step=1
)
# Taux d'impôt
taux_impot = st.sidebar.number_input(
    "Taux d'impôt (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1
)
# Nombre d'associés
nb_associés = st.sidebar.number_input(
    "Nombre d'associés", min_value=1, max_value=10, value=2, step=1
)

# Charges mensuelles fixes
st.sidebar.subheader("💼 Charges mensuelles fixes")\loyer = st.sidebar.number_input("Loyer (€)", min_value=0.0, value=1000.0, step=50.0)
salaires = st.sidebar.number_input("Salaires (€)", min_value=0.0, value=2000.0, step=100.0)
electricite = st.sidebar.number_input("Électricité (€)", min_value=0.0, value=200.0, step=10.0)
menage = st.sidebar.number_input("Ménage (€)", min_value=0.0, value=100.0, step=10.0)
pub = st.sidebar.number_input("Publicité (€)", min_value=0.0, value=150.0, step=10.0)
divers = st.sidebar.number_input("Divers (€)", min_value=0.0, value=100.0, step=10.0)
internet = st.sidebar.number_input("Internet (€)", min_value=0.0, value=50.0, step=5.0)

# Section produits
st.sidebar.header("🍽️ Produits vendus")
produits = [
    "Crêpe", "Gaufre", "Pancake", "Glace", "Salade/Bowl", "Jus", "Boisson chaude"
]

data_produits = []
for prod in produits:
    st.sidebar.subheader(f"📦 {prod}")
    prix = st.sidebar.number_input(f"Prix de vente unitaire {prod} (€)", min_value=0.0, value=5.0, step=0.1, key=f"prix_{prod}")
    cout = st.sidebar.number_input(f"Coût unitaire {prod} (€)", min_value=0.0, value=2.0, step=0.1, key=f"cout_{prod}")
    commandes = st.sidebar.number_input(f"Commandes par jour {prod}", min_value=0, value=20, step=1, key=f"cmd_{prod}")
    data_produits.append({
        "Produit": prod,
        "Prix_Unitaire": prix,
        "Coût_Unitaire": cout,
        "Commandes_Jour": commandes
    })

# Section charges d'investissement
st.sidebar.header("🏗️ Charges d'investissement")
nb_inv = st.sidebar.number_input("Nombre de charges d'investissement", min_value=0, max_value=10, value=0, step=1)
inv_list = []
for i in range(nb_inv):
    nom_inv = st.sidebar.text_input(f"Nom investissement {i+1}", key=f"inv_nom_{i}")
    val_inv = st.sidebar.number_input(f"Montant investissement {i+1} (€)", min_value=0.0, value=0.0, step=10.0, key=f"inv_val_{i}")
    inv_list.append({"Investissement": nom_inv or f"Investissement {i+1}", "Montant": val_inv})

# --- CALCULS ---
# DataFrame des produits
df_prod = pd.DataFrame(data_produits)

# Calculs variables
df_prod["Revenu_Mensuel"] = df_prod["Prix_Unitaire"] * df_prod["Commandes_Jour"] * jours_par_mois

df_prod["Coût_Mensuel"] = df_prod["Coût_Unitaire"] * df_prod["Commandes_Jour"] * jours_par_mois

revenu_brut = df_prod["Revenu_Mensuel"].sum()
cout_variable = df_prod["Coût_Mensuel"].sum()
cout_fixe = loyer + salaires + electricite + menage + pub + divers + internet
cout_total = cout_variable + cout_fixe

benefice_brut = revenu_brut - cout_total
montant_impot = benefice_brut * (taux_impot / 100)
profit_net = benefice_brut - montant_impot
part_par_associe = profit_net / nb_associés

# DataFrame résumé
resumé = pd.DataFrame({
    "Indicateur": [
        "Revenu brut (€)", "Coût total (€)", "Bénéfice avant impôt (€)",
        "Impôt (€)", "Profit net (€)", "Part par associé (€)"
    ],
    "Valeur": [
        revenu_brut, cout_total, benefice_brut,
        montant_impot, profit_net, part_par_associe
    ]
})

# DataFrame investissements
if inv_list:
    df_inv = pd.DataFrame(inv_list)
    total_invest = df_inv["Montant"].sum()
else:
    df_inv = pd.DataFrame(columns=["Investissement", "Montant"])
    total_invest = 0.0

# --- AFFICHAGE ---
st.markdown("---")
st.subheader("📋 Résumé financier mensuel")
st.table(resumé)

# Graphique barres
st.subheader("📈 Visualisation")
fig, ax = plt.subplots()
ax.bar(
    ["Revenu brut", "Coût total", "Profit net"],
    [revenu_brut, cout_total, profit_net]
)
ax.set_ylabel("Montant (€)")
ax.set_title("Comparatif des indicateurs clés")
st.pyplot(fig)

# Section investissements
if not df_inv.empty:
    st.markdown("---")
    st.subheader("🏗️ Détail des charges d'investissement")
    st.table(df_inv)
    st.write(f"**Total Investissement :** €{total_invest:,.2f}")

st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by Streamlit</p>", unsafe_allow_html=True)
