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
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
    }
    .positive-value {
        color: #28a745;
    }
    .negative-value {
        color: #dc3545;
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
            f"Prix de vente (Dh)",
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
            f"Coût unitaire (Dh)",
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
        f"{emoji} {charge} (Dh)",
        min_value=0.0,
        value=float(valeur_defaut),
        step=10.0,
        format="%.2f"
    )

# Charges d'investissement (nouvelle version)
st.sidebar.markdown("### 🏗️ Inventaire des charges d'investissement")

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
total_investissement = sum(charges_investissement_inputs.values())

# Contenu principal
col1, col2 = st.columns([2, 1])

with col1:
    # Affichage bien visible du total des profits nets
    st.markdown("## 💰 Résumé financier")
    col_profit1, col_profit2, col_profit3 = st.columns(3)
    with col_profit1:
        st.metric(label="Profit Net Total", value=f"{profit_net:.2f} Dh", 
                delta=f"{profit_net:.1f} Dh" if profit_net > 0 else f"-{abs(profit_net):.1f} Dh")
    with col_profit2:
        st.metric(label="Par Associé", value=f"{profit_par_associe:.2f} Dh")
    with col_profit3:
        roi = (profit_net * 12 / total_investissement * 100) if total_investissement > 0 else 0
        st.metric(label="ROI annuel", value=f"{roi:.2f}%")
    
    st.markdown('<p class="sub-header">📊 Tableau de bord financier</p>', unsafe_allow_html=True)
    
    # Tableau résumé des indicateurs financiers
    data_resume = {
        "Indicateur": ["Revenu brut mensuel", "Coût variable (produits)", "Coût fixe (charges)",
                         "Coût total mensuel", "Bénéfice avant impôt", f"Impôt ({taux_impot}%)",
                         "Profit net mensuel", f"Profit par associé ({nb_associes})"],
        "Montant (Dh)": [revenu_brut, cout_variable, cout_fixe, cout_total,
                          benefice_brut, impot, profit_net, profit_par_associe]
    }
    
    df_resume = pd.DataFrame(data_resume)
    df_resume["Montant (Dh)"] = df_resume["Montant (Dh)"].apply(lambda x: f"{x:.2f} Dh")
    
    st.dataframe(df_resume, use_container_width=True)
    
    # Tableau détaillé des produits
    st.markdown('<p class="sub-header">🍽️ Détails par produit</p>', unsafe_allow_html=True)
    
    data_produits = {
        "Produit": [f"{emoji} {produit}" for produit, emoji in zip(produits.keys(), produits.values())],
        "Prix unitaire (Dh)": [prix_vente[produit] for produit in produits],
        "Coût unitaire (Dh)": [cout_unitaire[produit] for produit in produits],
        "Marge unitaire (Dh)": [prix_vente[produit] - cout_unitaire[produit] for produit in produits],
        "Commandes/jour": [commandes_jour[produit] for produit in produits],
        "Revenu mensuel (Dh)": [revenus_produits[produit] for produit in produits],
        "Coût mensuel (Dh)": [couts_produits[produit] for produit in produits],
        "Marge mensuelle (Dh)": [marges_produits[produit] for produit in produits]
    }
    
    df_produits = pd.DataFrame(data_produits)
    
    # Formater les valeurs monétaires
    colonnes_monetaires = ["Prix unitaire (Dh)", "Coût unitaire (Dh)", "Marge unitaire (Dh)",
                          "Revenu mensuel (Dh)", "Coût mensuel (Dh)", "Marge mensuelle (Dh)"]
    for col in colonnes_monetaires:
        df_produits[col] = df_produits[col].apply(lambda x: f"{x:.2f} Dh")
    
    st.dataframe(df_produits, use_container_width=True)
    
    # Ligne de total séparée pour une meilleure visibilité
    st.markdown("### Total des produits")
    total_col1, total_col2, total_col3, total_col4 = st.columns(4)
    
    with total_col1:
        st.metric(label="Commandes totales / jour", 
                 value=f"{sum(commandes_jour.values())}")
    with total_col2:
        st.metric(label="Revenu mensuel total", 
                 value=f"{sum(revenus_produits.values()):.2f} Dh")
    with total_col3:
        st.metric(label="Coût mensuel total", 
                 value=f"{sum(couts_produits.values()):.2f} Dh")
    with total_col4:
        total_marge = sum(marges_produits.values())
        st.metric(label="Marge mensuelle totale", 
                 value=f"{total_marge:.2f} Dh",
                 delta=f"{total_marge:.1f}" if total_marge > 0 else f"-{abs(total_marge):.1f}")

with col2:
    # Visualisation du profit net
    st.markdown('<p class="sub-header">💹 Répartition financière</p>', unsafe_allow_html=True)
    
    # Préparation des données pour le graphique
    labels = ['Revenu brut', 'Coût total', 'Bénéfice brut', 'Impôt', 'Profit net']
    values = [revenu_brut, cout_total, benefice_brut, impot, profit_net]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values)
    
    # Coloriser les barres selon les valeurs positives/négatives
    for i, bar in enumerate(bars):
        if values[i] < 0:
            bar.set_color('#dc3545')  # Rouge pour valeurs négatives
        else:
            bar.set_color('#28a745')  # Vert pour valeurs positives
    
    plt.ylabel('Montant (Dh)')
    plt.title('Répartition financière mensuelle')
    
    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{height:.2f} Dh', ha='center', va='bottom')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)
    
    # Tableau des charges mensuelles
    st.markdown('<p class="sub-header">💸 Détail des charges mensuelles</p>', unsafe_allow_html=True)
    
    data_charges = {
        "Charge": [f"{emoji} {charge}" for charge, (emoji, _) in charges.items()],
        "Montant (Dh)": [charges_mensuelles[charge] for charge in charges]
    }
    
    df_charges = pd.DataFrame(data_charges)
    df_charges["Montant (Dh)"] = df_charges["Montant (Dh)"].apply(lambda x: f"{x:.2f} Dh")
    
    st.dataframe(df_charges, use_container_width=True)
    
    # Total des charges affiché de manière visible
    st.metric(label="Total des charges fixes", 
             value=f"{sum(charges_mensuelles.values()):.2f} Dh")
    
    # Tableau des investissements (Bonus)
    st.markdown('<p class="sub-header">🏗️ Charges d\'investissement</p>', unsafe_allow_html=True)
    
    data_inv = {
        "Investissement": list(charges_investissement_inputs.keys()),
        "Montant (Dh)": list(charges_investissement_inputs.values())
    }
    
    df_inv = pd.DataFrame(data_inv)
    df_inv["Montant (Dh)"] = df_inv["Montant (Dh)"].apply(lambda x: f"{x:.2f} Dh")
    
    st.dataframe(df_inv, use_container_width=True)
    
    # Total des investissements affiché de manière visible
    st.metric(label="Total des investissements", 
             value=f"{total_investissement:.2f} Dh")

# Graphique en camembert pour la répartition des coûts
st.markdown('<p class="sub-header">📉 Répartition des coûts</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Camembert des coûts variables par produit
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    labels_produits = [f"{emoji} {produit}" for produit, emoji in zip(produits.keys(), produits.values())]
    valeurs = [couts_produits[produit] for produit in produits]
    
    # Filtrer les produits sans coûts pour une meilleure lisibilité
    filtered_labels = []
    filtered_values = []
    for label, value in zip(labels_produits, valeurs):
        if value > 0:
            filtered_labels.append(label)
            filtered_values.append(value)
    
    if sum(filtered_values) > 0:
        ax1.pie(filtered_values, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.title('Répartition des coûts variables par produit')
        st.pyplot(fig1)
    else:
        st.warning("Aucun coût variable à afficher. Veuillez définir des produits avec des coûts.")

with col2:
    # Camembert des charges fixes
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    labels_charges = [f"{emoji} {charge}" for charge, (emoji, _) in charges.items()]
    valeurs_charges = [charges_mensuelles[charge] for charge in charges]
    
    # Filtrer les charges sans montants pour une meilleure lisibilité
    filtered_labels_charges = []
    filtered_values_charges = []
    for label, value in zip(labels_charges, valeurs_charges):
        if value > 0:
            filtered_labels_charges.append(label)
            filtered_values_charges.append(value)
    
    if sum(filtered_values_charges) > 0:
        ax2.pie(filtered_values_charges, labels=filtered_labels_charges, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        plt.title('Répartition des charges fixes mensuelles')
        st.pyplot(fig2)
    else:
        st.warning("Aucune charge fixe à afficher. Veuillez définir des charges avec des montants.")

# Analyse de rentabilité
st.markdown('<p class="sub-header">📈 Analyse de rentabilité</p>', unsafe_allow_html=True)

# Utilisation de colonnes pour une meilleure organisation
col1, col2 = st.columns(2)

with col1:
    # Calcul du point mort (seuil de rentabilité)
    if revenu_brut > 0:
        seuil_rentabilite = cout_fixe / (1 - (cout_variable / revenu_brut))
        st.metric(label="Seuil de rentabilité mensuel", value=f"{seuil_rentabilite:.2f} Dh")
        st.metric(label="Marge sur coût variable", value=f"{(1 - (cout_variable / revenu_brut)) * 100:.2f}%")

with col2:
    # Calcul du ROI
    if total_investissement > 0:
        roi_mensuel = profit_net / total_investissement * 100
        roi_annuel = roi_mensuel * 12
        temps_retour = total_investissement / profit_net if profit_net > 0 else float('inf')
        
        st.metric(label="ROI mensuel", value=f"{roi_mensuel:.2f}%")
        st.metric(label="ROI annuel", value=f"{roi_annuel:.2f}%")
        
        if profit_net > 0:
            st.metric(label="Temps de retour sur investissement", 
                     value=f"{temps_retour:.1f} mois ({temps_retour/12:.1f} ans)")
        else:
            st.warning("Le profit net est négatif ou nul, impossible de calculer le temps de retour sur investissement.")
    else:
        st.warning("Veuillez définir des charges d'investissement pour calculer le ROI.")

# Affichage d'un rapport final et des recommandations
st.markdown('<p class="sub-header">🔍 Rapport final et recommandations</p>', unsafe_allow_html=True)

if profit_net > 0:
    st.success("✅ **Votre projet est rentable!**")
    
    # Calcul des produits les plus rentables
    marges_produits_list = [(p, marges_produits[p]) for p in produits]
    marges_produits_list.sort(key=lambda x: x[1], reverse=True)
    
    st.markdown("### 🏆 Produits les plus rentables:")
    for i, (produit, marge) in enumerate(marges_produits_list[:3]):
        if marge > 0:
            st.markdown(f"{i+1}. **{produits[produit]} {produit}** - Marge mensuelle: {marge:.2f} Dh")
    
    st.markdown("### 💡 Recommandations:")
    st.markdown("- Considérez d'augmenter les volumes de vente des produits les plus rentables")
    st.markdown("- Envisagez une expansion progressive après la période de retour sur investissement")
    st.markdown("- Surveillez régulièrement les coûts variables pour maintenir votre marge bénéficiaire")
else:
    st.error("⚠️ **Votre projet n'est pas rentable dans sa configuration actuelle.**")
    st.markdown("### 💡 Recommandations:")
    st.markdown("- Augmentez les prix de vente ou le volume des ventes")
    st.markdown("- Réduisez les coûts fixes ou les coûts variables")
    st.markdown("- Concentrez-vous sur les produits à plus forte marge")
    st.markdown("- Réévaluez les investissements initiaux")
