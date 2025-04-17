import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Configuration de la page
st.set_page_config(
    page_title="Simulateur Business Plan Alimentaire",
    page_icon="📊",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stDataFrame {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .css-1aumxhk {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Titre de l'application
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📊 Simulateur Business Plan Alimentaire</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>Crêperie | Salon de Jus | Sucreries</h3>", unsafe_allow_html=True)

# Sidebar - Paramètres d'entrée
with st.sidebar:
    st.markdown("## 🛠️ Paramètres du Business")
    
    st.markdown("### 🍽️ Produits")
    produits = {
        "Crêpe": {"icon": "🥞"},
        "Gaufre": {"icon": "🧇"},
        "Pancake": {"icon": "🥞"},
        "Glace": {"icon": "🍦"},
        "Salade/Bowl": {"icon": "🥗"},
        "Jus": {"icon": "🧃"},
        "Boisson chaude": {"icon": "☕"}
    }
    
    for produit, data in produits.items():
        st.markdown(f"#### {data['icon']} {produit}")
        produits[produit]["prix"] = st.number_input(
            f"Prix de vente ({produit})", 
            min_value=0.0, 
            value=5.0 if produit in ["Crêpe", "Gaufre", "Pancake"] else 3.0,
            key=f"prix_{produit}"
        )
        produits[produit]["cout"] = st.number_input(
            f"Coût unitaire ({produit})", 
            min_value=0.0, 
            value=1.5 if produit in ["Crêpe", "Gaufre", "Pancake"] else 1.0,
            key=f"cout_{produit}"
        )
        produits[produit]["commandes"] = st.number_input(
            f"Commandes/jour ({produit})", 
            min_value=0, 
            value=20 if produit in ["Crêpe", "Gaufre", "Pancake"] else 15,
            key=f"cmd_{produit}"
        )
    
    st.markdown("### 📅 Activité")
    jours_activite = st.number_input("Nombre de jours d'activité/mois", min_value=1, max_value=31, value=26)
    taux_impot = st.number_input("Taux d'imposition (%)", min_value=0.0, max_value=100.0, value=25.0)
    nb_associes = st.number_input("Nombre d'associés", min_value=1, value=2)
    
    st.markdown("### 💰 Charges fixes mensuelles")
    charges = {
        "Loyer": st.number_input("Loyer (€)", min_value=0, value=1500),
        "Salaires": st.number_input("Salaires (€)", min_value=0, value=4000),
        "Électricité": st.number_input("Électricité (€)", min_value=0, value=300),
        "Ménage": st.number_input("Ménage (€)", min_value=0, value=200),
        "Publicité": st.number_input("Publicité (€)", min_value=0, value=300),
        "Divers": st.number_input("Divers (€)", min_value=0, value=500),
        "Internet": st.number_input("Internet (€)", min_value=0, value=50)
    }
    
    st.markdown("### 🏦 Investissements (optionnel)")
    investissements = {
        "Matériel": st.number_input("Matériel (€)", min_value=0, value=0),
        "Aménagement": st.number_input("Aménagement (€)", min_value=0, value=0),
        "Dépôt de garantie": st.number_input("Dépôt de garantie (€)", min_value=0, value=0),
        "Autres": st.number_input("Autres investissements (€)", min_value=0, value=0)
    }

# Calcul des indicateurs financiers
def calculer_indicateurs():
    # Calcul des revenus et coûts par produit
    revenu_brut = 0
    cout_total_produits = 0
    
    details_produits = []
    for produit, data in produits.items():
        revenu_produit = data["prix"] * data["commandes"] * jours_activite
        cout_produit = data["cout"] * data["commandes"] * jours_activite
        revenu_brut += revenu_produit
        cout_total_produits += cout_produit
        
        details_produits.append({
            "Produit": produit,
            "Revenu": revenu_produit,
            "Coût": cout_produit,
            "Marge": revenu_produit - cout_produit
        })
    
    # Calcul des charges totales
    charges_totales = sum(charges.values())
    
    # Calcul du bénéfice avant impôt
    benefice_avant_impot = revenu_brut - cout_total_produits - charges_totales
    
    # Calcul de l'impôt
    impot = benefice_avant_impot * (taux_impot / 100)
    
    # Calcul du profit net
    profit_net = benefice_avant_impot - impot
    
    # Calcul de la part par associé
    part_associe = profit_net / nb_associes if nb_associes > 0 else 0
    
    # Calcul des investissements totaux
    total_investissements = sum(investissements.values())
    
    return {
        "revenu_brut": revenu_brut,
        "cout_total_produits": cout_total_produits,
        "charges_totales": charges_totales,
        "benefice_avant_impot": benefice_avant_impot,
        "impot": impot,
        "profit_net": profit_net,
        "part_associe": part_associe,
        "details_produits": details_produits,
        "total_investissements": total_investissements
    }

# Affichage des résultats
resultats = calculer_indicateurs()

# Tableau récapitulatif des indicateurs financiers
st.markdown("## 📈 Résultats Financiers Mensuels")

indicateurs = pd.DataFrame({
    "Indicateur": [
        "Revenu brut mensuel", 
        "Coût total des produits", 
        "Charges fixes mensuelles",
        "Bénéfice avant impôt", 
        "Impôt (" + str(taux_impot) + "%)", 
        "Profit net mensuel",
        "Profit net par associé (" + str(nb_associes) + " associés)"
    ],
    "Montant (€)": [
        resultats["revenu_brut"],
        resultats["cout_total_produits"],
        resultats["charges_totales"],
        resultats["benefice_avant_impot"],
        resultats["impot"],
        resultats["profit_net"],
        resultats["part_associe"]
    ]
})

# Formatage des montants en euros
indicateurs["Montant (€)"] = indicateurs["Montant (€)"].apply(lambda x: f"{x:,.2f} €")

st.dataframe(
    indicateurs,
    column_config={
        "Indicateur": "Indicateur",
        "Montant (€)": "Montant"
    },
    hide_index=True,
    use_container_width=True
)

# Graphique des résultats
st.markdown("## 📊 Visualisation des Résultats")

fig, ax = plt.subplots(figsize=(10, 6))

categories = ["Revenus", "Coûts", "Bénéfice"]
valeurs = [
    resultats["revenu_brut"],
    resultats["cout_total_produits"] + resultats["charges_totales"],
    resultats["profit_net"]
]

colors = ["#2ecc71", "#e74c3c", "#3498db"]
bars = ax.bar(categories, valeurs, color=colors)

# Ajout des valeurs sur les barres
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:,.0f} €',
            ha='center', va='bottom')

# Formatage de l'axe Y en euros
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:,.0f} €'))

ax.set_title("Résultats Financiers Mensuels", pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# Détails par produit
st.markdown("## 🍽️ Performance par Produit")

details_df = pd.DataFrame(resultats["details_produits"])
details_df["Revenu"] = details_df["Revenu"].apply(lambda x: f"{x:,.2f} €")
details_df["Coût"] = details_df["Coût"].apply(lambda x: f"{x:,.2f} €")
details_df["Marge"] = details_df["Marge"].apply(lambda x: f"{x:,.2f} €")

st.dataframe(
    details_df,
    column_config={
        "Produit": "Produit",
        "Revenu": "Revenu",
        "Coût": "Coût",
        "Marge": "Marge"
    },
    hide_index=True,
    use_container_width=True
)

# Section investissements (optionnel)
if any(value > 0 for value in investissements.values()):
    st.markdown("## 🏦 Investissements")
    
    invest_df = pd.DataFrame({
        "Type": list(investissements.keys()),
        "Montant (€)": list(investissements.values())
    })
    
    invest_df["Montant (€)"] = invest_df["Montant (€)"].apply(lambda x: f"{x:,.2f} €")
    
    st.dataframe(
        invest_df,
        column_config={
            "Type": "Type d'investissement",
            "Montant (€)": "Montant"
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown(f"**Total des investissements : {resultats['total_investissements']:,.2f} €**")

# Notes et informations supplémentaires
with st.expander("ℹ️ Notes et informations"):
    st.markdown("""
        - **Revenu brut mensuel** : Somme des ventes de tous les produits
        - **Coût total des produits** : Coût des matières premières pour tous les produits vendus
        - **Charges fixes** : Dépenses mensuelles récurrentes (loyer, salaires, etc.)
        - **Bénéfice avant impôt** : Revenu brut - Coût des produits - Charges fixes
        - **Impôt** : Calculé sur le bénéfice avant impôt selon le taux spécifié
        - **Profit net** : Bénéfice après déduction de l'impôt
    """)
