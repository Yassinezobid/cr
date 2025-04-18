import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="SimuProfit - Business Plan",
    page_icon="🍽️",
    layout="wide"
)

# Fonction pour ajouter un style CSS personnalisé
def local_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4ECDC4;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #495057;
    }
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
    }
    .table-header {
        font-weight: bold;
        background-color: #4ECDC4 !important;
        color: white !important;
    }
    .positive-value {
        color: #28a745;
        font-weight: bold;
    }
    .negative-value {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Titre principal de l'application
st.markdown('<p class="main-header">🍽️ SimuProfit - Business Plan Mensuel</p>', unsafe_allow_html=True)
st.markdown("### Simulez la rentabilité de votre commerce alimentaire en quelques clics")

# Sidebar - Paramètres d'entrée
st.sidebar.markdown("## ⚙️ Paramètres de simulation")

# Définition des produits
st.sidebar.markdown("### 🍽️ Produits proposés")

# Liste des produits avec leurs emojis
produits = {
    "Crêpes": "🥞",
    "Gaufres": "🧇",
    "Pancakes": "🥮",
    "Glaces": "🍦",
    "Salades/Bowls": "🥗",
    "Jus": "🧃",
    "Boissons chaudes": "☕"
}

# Dictionnaires pour stocker les informations par produit
prix_vente = {}
cout_unitaire = {}
commandes_jour = {}

# Création des champs pour chaque produit
for produit, emoji in produits.items():
    st.sidebar.markdown(f"#### {emoji} {produit}")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        prix_vente[produit] = st.number_input(
            f"Prix de vente (€)",
            min_value=0.0,
            value=30.0 if "Crêpes" in produit else (
                25.0 if "Gaufres" in produit else (
                25.0 if "Pancakes" in produit else (
                14.0 if "Glaces" in produit else (
                25.0 if "Salades" in produit else (
                18.0 if "Jus" in produit else 3.0
                ))))),
            step=0.5,
            format="%.2f",
            key=f"prix_{produit}"
        )
        
    with col2:
        cout_unitaire[produit] = st.number_input(
            f"Coût unitaire (€)",
            min_value=0.0,
            value=8.0 if "Crêpes" in produit else (
                8.0 if "Gaufres" in produit else (
                7.0 if "Pancakes" in produit else (
                4.0 if "Glaces" in produit else (
                14.0 if "Salades" in produit else (
                8.0 if "Jus" in produit else 0.8
                ))))),
            step=0.1,
            format="%.2f",
            key=f"cout_{produit}"
        )
    
    commandes_jour[produit] = st.sidebar.number_input(
        f"Commandes par jour",
        min_value=0,
        value=int(25) if "Crêpes" in produit else (
            int(15) if "Gaufres" in produit else (
            int(12) if "Pancakes" in produit else (
            int(20) if "Glaces" in produit else (
            int(10) if "Salades" in produit else (
            int(10) if "Jus" in produit else int(40)
            ))))),
        step=1,
        key=f"commandes_{produit}"
    )
    st.sidebar.markdown("---")

# Paramètres généraux
st.sidebar.markdown("### 📆 Paramètres d'activité")
jours_activite = st.sidebar.number_input(
    "Nombre de jours d'activité par mois",
    min_value=1,
    max_value=31,
    value=26,
    step=1
)

taux_impot = st.sidebar.slider(
    "Taux d'impôt (%)",
    min_value=0.0,
    max_value=50.0,
    value=20.0,
    step=0.5
)

nb_associes = st.sidebar.number_input(
    "Nombre d'associés",
    min_value=1,
    value=2,
    step=1
)

# Charges mensuelles
st.sidebar.markdown("### 💰 Charges mensuelles fixes")

charges = {
    "Loyer": ("🏢", 1200),
    "Salaires": ("👨‍🍳", 3500),
    "Électricité": ("⚡", 300),
    "Ménage": ("🧹", 200),
    "Publicité": ("📱", 150),
    "Internet": ("🌐", 60),
    "Divers": ("📦", 200)
}

charges_mensuelles = {}
for charge, (emoji, valeur_defaut) in charges.items():
    charges_mensuelles[charge] = st.sidebar.number_input(
        f"{emoji} {charge} (€)",
        min_value=0.0,
        value=float(valeur_defaut),
        step=10.0,
        format="%.2f"
    )

# Charges d'investissement (nouvelle version)
st.sidebar.markdown("### 🏗️ Inventaire des charges d’investissement")

charges_investissement = {
    # Équipements
    "Crépier": 7000,
    "Gauffrel": 3750,
    "Plaque & Pancakes": 650,
    "Blender": 1500,
    "Extracteur de jus": 2250,
    "Machine café": 30000,
    "Vitrine 2 glaces": 17500,
    "Réfrigérateur": 5000,
    "Congélateur": 3000,
    "Presse agrume": 1750,
    "Ustensiles": 4000,
    "Produits initiales": 20000,

    # Aménagement / Design Intérieur
    "Peinture & Travaux": 10000,
    "Décoration & Lumières": 20000,
    "Étagères": 3500,
    "Comptoir": 5000,
    "Tables + Chaises": 2500,
    "Panneaux extérieurs": 10000,
    "TV + Caisse enregistreuse": 10000,
    "Caméras de surveillance": 3000,

    # Divers
    "Loyer": 18000,
    "Publicités": 15000
}

charges_investissement_inputs = {}
for inv, montant in charges_investissement.items():
    charges_investissement_inputs[inv] = st.sidebar.number_input(
        f"{inv}",
        min_value=0.0,
        value=float(montant),
        step=100.0,
        format="%.2f"
    )

# Calculs financiers
# Calcul des revenus et coûts par produit
revenus_produits = {}
couts_produits = {}
marges_produits = {}

for produit in produits:
    revenus_produits[produit] = prix_vente[produit] * commandes_jour[produit] * jours_activite
    couts_produits[produit] = cout_unitaire[produit] * commandes_jour[produit] * jours_activite
    marges_produits[produit] = revenus_produits[produit] - couts_produits[produit]

# Calcul des totaux
revenu_brut = sum(revenus_produits.values())
cout_variable = sum(couts_produits.values())
cout_fixe = sum(charges_mensuelles.values())
cout_total = cout_variable + cout_fixe
benefice_brut = revenu_brut - cout_total
impot = benefice_brut * (taux_impot / 100) if benefice_brut > 0 else 0
profit_net = benefice_brut - impot
profit_par_associe = profit_net / nb_associes if nb_associes > 0 else 0

# Total des investissements
total_investissement = sum(charges_investissement.values())

# Contenu principal
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="sub-header">📊 Tableau de bord financier</p>', unsafe_allow_html=True)
    
    # Tableau résumé des indicateurs financiers
    data_resume = {
        "Indicateur": ["Revenu brut mensuel", "Coût variable (produits)", "Coût fixe (charges)",
                     "Coût total mensuel", "Bénéfice avant impôt", f"Impôt ({taux_impot}%)",
                     "Profit net mensuel", f"Profit par associé ({nb_associes})"],
        "Montant (€)": [revenu_brut, cout_variable, cout_fixe, cout_total,
                      benefice_brut, impot, profit_net, profit_par_associe]
    }
    
    df_resume = pd.DataFrame(data_resume)
    
    # Formater les valeurs monétaires
    df_resume["Montant (€)"] = df_resume["Montant (€)"].apply(lambda x: f"{x:.2f} €")
    
    # Appliquer un style au tableau
    def style_tableau_resume(df):
        return df.style.apply(lambda x: ['background-color: #f8f9fa' for _ in x], axis=1)\
                      .set_properties(**{'text-align': 'center'})
    
    st.table(style_tableau_resume(df_resume))
    
    # Tableau détaillé des produits
    st.markdown('<p class="sub-header">🍽️ Détails par produit</p>', unsafe_allow_html=True)
    
    data_produits = {
        "Produit": [f"{emoji} {produit}" for produit, emoji in zip(produits.keys(), produits.values())],
        "Prix unitaire (€)": [prix_vente[produit] for produit in produits],
        "Coût unitaire (€)": [cout_unitaire[produit] for produit in produits],
        "Marge unitaire (€)": [prix_vente[produit] - cout_unitaire[produit] for produit in produits],
        "Commandes/jour": [commandes_jour[produit] for produit in produits],
        "Revenu mensuel (€)": [revenus_produits[produit] for produit in produits],
        "Coût mensuel (€)": [couts_produits[produit] for produit in produits],
        "Marge mensuelle (€)": [marges_produits[produit] for produit in produits]
    }
    
    df_produits = pd.DataFrame(data_produits)
    
    # Formater les valeurs monétaires
    colonnes_monetaires = ["Prix unitaire (€)", "Coût unitaire (€)", "Marge unitaire (€)",
                          "Revenu mensuel (€)", "Coût mensuel (€)", "Marge mensuelle (€)"]
    for col in colonnes_monetaires:
        df_produits[col] = df_produits[col].apply(lambda x: f"{x:.2f} €")
    
    st.table(df_produits)

with col2:
    # Visualisation du profit net
    st.markdown('<p class="sub-header">💹 Répartition financière</p>', unsafe_allow_html=True)
    
    # Préparation des données pour le graphique
    labels = ['Revenu brut', 'Coût total', 'Bénéfice brut', 'Impôt', 'Profit net']
    values = [revenu_brut, cout_total, benefice_brut, impot, profit_net]
    colors = ['#4ECDC4', '#FF6B6B', '#FFD166', '#073B4C', '#06D6A0']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors)
    
    plt.ylabel('Montant (€)')
    plt.title('Répartition financière mensuelle')
    
    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{height:.2f} €', ha='center', va='bottom')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)
    
    # Tableau des charges mensuelles
    st.markdown('<p class="sub-header">💸 Détail des charges mensuelles</p>', unsafe_allow_html=True)
    
    data_charges = {
        "Charge": [f"{emoji} {charge}" for charge, (emoji, _) in charges.items()],
        "Montant (€)": [charges_mensuelles[charge] for charge in charges]
    }
    
    df_charges = pd.DataFrame(data_charges)
    df_charges["Montant (€)"] = df_charges["Montant (€)"].apply(lambda x: f"{x:.2f} €")
    
    # Ajouter une ligne de total
    df_charges.loc[len(df_charges)] = ["Total", f"{sum(charges_mensuelles.values()):.2f} €"]
    
    st.table(df_charges)
    
    # Tableau des investissements (Bonus)
    st.markdown('<p class="sub-header">🏗️ Charges d\'investissement</p>', unsafe_allow_html=True)
    
    data_inv = {
        "Investissement": list(charges_investissement_inputs.keys()),
        "Montant": list(charges_investissement_inputs.values())
    }
    
    df_inv = pd.DataFrame(data_inv)
    df_inv["Montant"] = df_inv["Montant"].apply(lambda x: f"{x:.2f}")
    df_inv.loc[len(df_inv)] = ["Total", f"{sum(charges_investissement_inputs.values()):.2f}"]
    
    st.table(df_inv)

# Graphique en camembert pour la répartition des coûts
st.markdown('<p class="sub-header">📉 Répartition des coûts</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Camembert des coûts variables par produit
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    labels_produits = [f"{emoji} {produit}" for produit, emoji in zip(produits.keys(), produits.values())]
    valeurs = [couts_produits[produit] for produit in produits]
    
    # Utilisation des couleurs de matplotlib au lieu de seaborn
    colors = plt.cm.viridis(np.linspace(0, 1, len(labels_produits)))
    
    ax1.pie(valeurs, labels=labels_produits, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')
    plt.title('Répartition des coûts variables par produit')
    
    st.pyplot(fig1)

with col2:
    # Camembert des charges fixes
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    labels_charges = [f"{emoji} {charge}" for charge, (emoji, _) in charges.items()]
    valeurs_charges = [charges_mensuelles[charge] for charge in charges]
    
    # Utilisation des couleurs de matplotlib au lieu de seaborn
    colors2 = plt.cm.plasma(np.linspace(0, 1, len(labels_charges)))
    
    ax2.pie(valeurs_charges, labels=labels_charges, autopct='%1.1f%%', startangle=90, colors=colors2)
    ax2.axis('equal')
    plt.title('Répartition des charges fixes mensuelles')
    
    st.pyplot(fig2)

# Analyse de rentabilité
st.markdown('<p class="sub-header">📈 Analyse de rentabilité</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Marge par produit en graphique à barres horizontales
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    
    produits_liste = list(produits.keys())
    marges = [marges_produits[p] for p in produits_liste]
    
    # Trier par marge décroissante
    sorted_indices = np.argsort(marges)
    sorted_produits = [produits_liste[i] for i in sorted_indices]
    sorted_marges = [marges[i] for i in sorted_indices]
    sorted_emojis = [produits[p] for p in sorted_produits]
    
    # Couleurs basées sur les valeurs
    colors3 = plt.cm.RdYlGn(np.linspace(0, 1, len(sorted_produits)))
    
    bars = ax3.barh([f"{emoji} {p}" for p, emoji in zip(sorted_produits, sorted_emojis)], sorted_marges, color=colors3)
    
    # Ajouter les valeurs à la fin des barres
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x_pos = width + 20
        ax3.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.2f} €',
                ha='left', va='center')
    
    plt.xlabel('Marge mensuelle (€)')
    plt.title('Marge mensuelle par produit')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    st.pyplot(fig3)

with col2:
    # Indicateurs clés de performance
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🔑 Indicateurs clés de performance")
    
    # Calculer quelques KPIs
    marge_brute_pct = (revenu_brut - cout_variable) / revenu_brut * 100 if revenu_brut > 0 else 0
    marge_nette_pct = profit_net / revenu_brut * 100 if revenu_brut > 0 else 0
    ratio_cout_revenu = cout_total / revenu_brut * 100 if revenu_brut > 0 else 0
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Marge brute**")
        st.markdown(f"<span class='metric-value'>{marge_brute_pct:.1f}%</span>", unsafe_allow_html=True)
        
        st.markdown("**Marge nette**")
        st.markdown(f"<span class='metric-value'>{marge_nette_pct:.1f}%</span>", unsafe_allow_html=True)
    
    with col_b:
        st.markdown("**Ratio coût/revenu**")
        st.markdown(f"<span class='metric-value'>{ratio_cout_revenu:.1f}%</span>", unsafe_allow_html=True)
        
        st.markdown("**Seuil de rentabilité**")
        # Calcul simplifié du seuil de rentabilité
        seuil_rentabilite = cout_fixe / (marge_brute_pct/100) if marge_brute_pct > 0 else float('inf')
        st.markdown(f"<span class='metric-value'>{seuil_rentabilite:.2f} €</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analyse des produits rentables vs non rentables
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Produits les plus rentables")
    
    # Calculer la rentabilité par produit (marge unitaire)
    rentabilite_par_produit = {}
    for produit in produits:
        marge_unitaire = prix_vente[produit] - cout_unitaire[produit]
        marge_pct = (marge_unitaire / prix_vente[produit]) * 100 if prix_vente[produit] > 0 else 0
        rentabilite_par_produit[produit] = (marge_unitaire, marge_pct)
    
    # Trier par rentabilité
    produits_tries = sorted(rentabilite_par_produit.items(), key=lambda x: x[1][1], reverse=True)
    
    # Afficher les 3 premiers
    for i, (produit, (marge, pct)) in enumerate(produits_tries[:3]):
        st.markdown(f"**{i+1}. {produits[produit]} {produit}**: Marge {marge:.2f}€ ({pct:.1f}%)")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Pied de page
st.markdown("---")
st.markdown("### 💡 Recommandations")

# Générer des recommandations basées sur l'analyse
recommandations = []

# Recommandation basée sur les marges
produit_plus_rentable = max(rentabilite_par_produit.items(), key=lambda x: x[1][0])[0]
produit_moins_rentable = min(rentabilite_par_produit.items(), key=lambda x: x[1][0])[0]

recommandations.append(f"🔍 Augmenter la promotion du produit **{produit_plus_rentable}** qui a la meilleure marge unitaire.")
recommandations.append(f"🔍 Revoir la formule ou le prix du produit **{produit_moins_rentable}** qui présente la plus faible marge.")

# Recommandation basée sur le profit net
if profit_net <= 0:
    recommandations.append("⚠️ Le commerce n'est pas rentable actuellement. Examiner les possibilités de réduction des coûts fixes.")
elif marge_nette_pct < 10:
    recommandations.append("⚠️ La marge nette est inférieure à 10%. Envisager d'augmenter les prix ou de réduire les coûts.")
else:
    recommandations.append("✅ Le commerce présente une bonne rentabilité. Envisager des investissements pour développer l'activité.")

# Afficher les recommandations
for rec in recommandations:
    st.markdown(f"- {rec}")

st.markdown("---")
st.markdown("*Cette simulation est fournie à titre indicatif. Les résultats réels peuvent varier en fonction de nombreux facteurs.*")
