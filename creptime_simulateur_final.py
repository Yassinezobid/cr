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
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .profit-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .chart-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Titre principal de l'application
st.markdown('<p class="main-header">🍽️ SimuProfit - Business Plan Mensuel</p>', unsafe_allow_html=True)
st.markdown("### Simulez la rentabilité de votre commerce alimentaire en quelques clics")

# Initialisation des variables de session si elles n'existent pas déjà
if 'prix_vente' not in st.session_state:
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
    
    # Initialisation des dictionnaires dans la session
    st.session_state.produits = produits
    st.session_state.prix_vente = {
        "Crêpes": 30.0,
        "Gaufres": 25.0,
        "Pancakes": 25.0,
        "Glaces": 14.0,
        "Salades/Bowls": 25.0,
        "Jus": 18.0,
        "Boissons chaudes": 14.0
    }
    
    st.session_state.cout_unitaire = {
        "Crêpes": 8.0,
        "Gaufres": 8.0,
        "Pancakes": 7.0,
        "Glaces": 4.0,
        "Salades/Bowls": 14.0,
        "Jus": 8.0,
        "Boissons chaudes": 5.0
    }
    
    st.session_state.commandes_jour = {
        "Crêpes": 25,
        "Gaufres": 15,
        "Pancakes": 12,
        "Glaces": 20,
        "Salades/Bowls": 10,
        "Jus": 10,
        "Boissons chaudes": 40
    }
    
    # Initialisation des paramètres d'activité
    st.session_state.jours_activite = 30
    st.session_state.taux_impot = 20.0
    st.session_state.nb_associes = 6
    
    # Initialisation des charges mensuelles
    st.session_state.charges_mensuelles = {
        "Loyer": 7000.0,
        "Salaires": 6000.0,
        "Électricité": 3000.0,
        "Ménage": 500.0,
        "Publicité": 2000.0,
        "Internet": 400.0,
        "Divers": 1000.0
    }
    
    # Initialisation des charges d'investissement
    st.session_state.charges_investissement = {
        # Équipements
        "Crépier": 7000.0,
        "Gauffrel": 3750.0,
        "Plaque & Pancakes": 650.0,
        "Blender": 1500.0,
        "Extracteur de jus": 2250.0,
        "Machine café": 30000.0,
        "Vitrine 2 glaces": 17500.0,
        "Réfrigérateur": 5000.0,
        "Congélateur": 3000.0,
        "Presse agrume": 1750.0,
        "Ustensiles": 4000.0,
        "Produits initiales": 20000.0,

        # Aménagement / Design Intérieur
        "Peinture & Travaux": 10000.0,
        "Décoration & Lumières": 20000.0,
        "Étagères": 3500.0,
        "Comptoir": 5000.0,
        "Tables + Chaises": 2500.0,
        "Panneaux extérieurs": 10000.0,
        "TV + Caisse enregistreuse": 10000.0,
        "Caméras de surveillance": 3000.0,

        # Divers
        "Loyer avance": 18000.0,
        "Publicités": 15000.0
    }

# Dictionnaire des emojis pour les charges
charges_emojis = {
    "Loyer": "🏢",
    "Salaires": "👨‍🍳",
    "Électricité": "⚡",
    "Ménage": "🧹",
    "Publicité": "📱",
    "Internet": "🌐",
    "Divers": "📦",
    "Loyer avance": "🏢"
}

# Sidebar masquée mais utilisable si nécessaire
with st.sidebar:
    st.markdown("### ⚙️ Paramètres supplémentaires")
    st.markdown("Utilisez directement les tableaux principaux pour modifier les valeurs")

# Fonction pour calculer les indicateurs financiers
def calculer_indicateurs():
    # Calcul des revenus et coûts par produit
    revenus_produits = {}
    couts_produits = {}
    marges_produits = {}

    for produit in st.session_state.produits:
        revenus_produits[produit] = st.session_state.prix_vente[produit] * st.session_state.commandes_jour[produit] * st.session_state.jours_activite
        couts_produits[produit] = st.session_state.cout_unitaire[produit] * st.session_state.commandes_jour[produit] * st.session_state.jours_activite
        marges_produits[produit] = revenus_produits[produit] - couts_produits[produit]

    # Calcul des totaux
    revenu_brut = sum(revenus_produits.values())
    cout_variable = sum(couts_produits.values())
    cout_fixe = sum(st.session_state.charges_mensuelles.values())
    cout_total = cout_variable + cout_fixe
    benefice_brut = revenu_brut - cout_total
    impot = benefice_brut * (st.session_state.taux_impot / 100) if benefice_brut > 0 else 0
    profit_net = benefice_brut - impot
    profit_par_associe = profit_net / st.session_state.nb_associes if st.session_state.nb_associes > 0 else 0
    
    # Total des investissements
    total_investissement = sum(st.session_state.charges_investissement.values())
    
    # Calcul du seuil de rentabilité
    if revenu_brut > 0:
        seuil_rentabilite = cout_fixe / (1 - (cout_variable / revenu_brut))
        marge_cout_variable = (1 - (cout_variable / revenu_brut)) * 100
    else:
        seuil_rentabilite = 0
        marge_cout_variable = 0
    
    # Calcul du ROI
    if total_investissement > 0 and profit_net > 0:
        roi_mensuel = profit_net / total_investissement * 100
        roi_annuel = roi_mensuel * 12
        temps_retour = total_investissement / profit_net
    else:
        roi_mensuel = 0
        roi_annuel = 0
        temps_retour = float('inf')
    
    return {
        'revenus_produits': revenus_produits,
        'couts_produits': couts_produits,
        'marges_produits': marges_produits,
        'revenu_brut': revenu_brut,
        'cout_variable': cout_variable,
        'cout_fixe': cout_fixe,
        'cout_total': cout_total,
        'benefice_brut': benefice_brut,
        'impot': impot,
        'profit_net': profit_net,
        'profit_par_associe': profit_par_associe,
        'total_investissement': total_investissement,
        'seuil_rentabilite': seuil_rentabilite,
        'marge_cout_variable': marge_cout_variable,
        'roi_mensuel': roi_mensuel,
        'roi_annuel': roi_annuel,
        'temps_retour': temps_retour
    }

# Calculer les indicateurs financiers
indicateurs = calculer_indicateurs()

# Contenu principal
# 1. Affichage du résumé financier
st.markdown("## 💰 Résumé financier")
col_profit1, col_profit2, col_profit3 = st.columns(3)
with col_profit1:
    st.metric(label="Profit Net Total", value=f"{indicateurs['profit_net']:.2f} Dh",
            delta=f"{indicateurs['profit_net']:.1f} Dh" if indicateurs['profit_net'] > 0 else f"-{abs(indicateurs['profit_net']):.1f} Dh")
with col_profit2:
    st.metric(label="Par Associé", value=f"{indicateurs['profit_par_associe']:.2f} Dh")
with col_profit3:
    st.metric(label="ROI annuel", value=f"{indicateurs['roi_annuel']:.2f}%")

# 2. Paramètres d'activité généraux (dans un formulaire éditable)
st.markdown('<p class="sub-header">📆 Paramètres d\'activité</p>', unsafe_allow_html=True)
params_col1, params_col2, params_col3 = st.columns(3)

with params_col1:
    jours_activite = st.number_input(
        "Nombre de jours d'activité par mois",
        min_value=1,
        max_value=31,
        value=st.session_state.jours_activite,
        step=1,
        key="jours_activite_input"
    )
    st.session_state.jours_activite = jours_activite

with params_col2:
    taux_impot = st.number_input(
        "Taux d'impôt (%)",
        min_value=0.0,
        max_value=50.0,
        value=st.session_state.taux_impot,
        step=0.5,
        key="taux_impot_input"
    )
    st.session_state.taux_impot = taux_impot

with params_col3:
    nb_associes = st.number_input(
        "Nombre d'associés",
        min_value=1,
        value=st.session_state.nb_associes,
        step=1,
        key="nb_associes_input"
    )
    st.session_state.nb_associes = nb_associes

# 3. Tableau de bord financier
st.markdown('<p class="sub-header">📊 Tableau de bord financier</p>', unsafe_allow_html=True)

# Visualisation du profit net
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['Revenu brut', 'Coût total', 'Bénéfice brut', 'Impôt', 'Profit net']
values = [
    indicateurs['revenu_brut'],
    indicateurs['cout_total'],
    indicateurs['benefice_brut'],
    indicateurs['impot'],
    indicateurs['profit_net']
]

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

# Affichage du graphique dans un container stylisé
with st.container():
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# Tableau résumé des indicateurs financiers
data_resume = {
    "Indicateur": ["Revenu brut mensuel", "Coût variable (produits)", "Coût fixe (charges)",
                     "Coût total mensuel", "Bénéfice avant impôt", f"Impôt ({st.session_state.taux_impot}%)",
                     "Profit net mensuel", f"Profit par associé ({st.session_state.nb_associes})"],
    "Montant (Dh)": [
        indicateurs['revenu_brut'],
        indicateurs['cout_variable'],
        indicateurs['cout_fixe'],
        indicateurs['cout_total'],
        indicateurs['benefice_brut'],
        indicateurs['impot'],
        indicateurs['profit_net'],
        indicateurs['profit_par_associe']
    ]
}

df_resume = pd.DataFrame(data_resume)
df_resume["Montant (Dh)"] = df_resume["Montant (Dh)"].apply(lambda x: f"{x:.2f} Dh")

st.dataframe(df_resume, use_container_width=True)

# 4. Tableau détaillé des produits (éditable)
st.markdown('<p class="sub-header">🍽️ Détails par produit</p>', unsafe_allow_html=True)

# Créer un DataFrame pour les produits avec les colonnes éditables
produits_data = []
for produit in st.session_state.produits:
    emoji = st.session_state.produits[produit]
    produits_data.append({
        "Produit": f"{emoji} {produit}",
        "Produit_key": produit,  # Clé pour référence
        "Prix unitaire (Dh)": st.session_state.prix_vente[produit],
        "Coût unitaire (Dh)": st.session_state.cout_unitaire[produit],
        "Commandes/jour": st.session_state.commandes_jour[produit],
        "Revenu mensuel (Dh)": indicateurs['revenus_produits'][produit],
        "Coût mensuel (Dh)": indicateurs['couts_produits'][produit],
        "Marge mensuelle (Dh)": indicateurs['marges_produits'][produit],
    })

df_produits = pd.DataFrame(produits_data)

# Utiliser un formulaire pour la modification
with st.form(key="produits_form"):
    # Table éditable pour les produits
    for i, row in enumerate(produits_data):
        st.markdown(f"#### {row['Produit']}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            prix = st.number_input(
                "Prix unitaire (Dh)",
                min_value=0.0,
                value=float(row['Prix unitaire (Dh)']),
                step=0.5,
                key=f"prix_{i}"
            )
        
        with col2:
            cout = st.number_input(
                "Coût unitaire (Dh)",
                min_value=0.0,
                value=float(row['Coût unitaire (Dh)']),
                step=0.1,
                key=f"cout_{i}"
            )
        
        with col3:
            commandes = st.number_input(
                "Commandes/jour",
                min_value=0,
                value=int(row['Commandes/jour']),
                step=1,
                key=f"commandes_{i}"
            )
        
        # Mise à jour des valeurs
        produit_key = row['Produit_key']
        st.session_state.prix_vente[produit_key] = prix
        st.session_state.cout_unitaire[produit_key] = cout
        st.session_state.commandes_jour[produit_key] = commandes
        
        st.markdown("---")
    
    # Bouton pour soumettre les modifications
    submitted = st.form_submit_button("Mettre à jour les calculs")
    if submitted:
        st.success("Valeurs mises à jour! Les calculs ont été recalculés.")
        indicateurs = calculer_indicateurs()  # Recalculer les indicateurs

# Affichage des résultats calculés pour les produits
# Recréer le DataFrame avec les valeurs mises à jour
produits_data_updated = []
for produit in st.session_state.produits:
    emoji = st.session_state.produits[produit]
    marge_unitaire = st.session_state.prix_vente[produit] - st.session_state.cout_unitaire[produit]
    revenu_mensuel = st.session_state.prix_vente[produit] * st.session_state.commandes_jour[produit] * st.session_state.jours_activite
    cout_mensuel = st.session_state.cout_unitaire[produit] * st.session_state.commandes_jour[produit] * st.session_state.jours_activite
    marge_mensuelle = revenu_mensuel - cout_mensuel
    
    produits_data_updated.append({
        "Produit": f"{emoji} {produit}",
        "Prix unitaire (Dh)": f"{st.session_state.prix_vente[produit]:.2f} Dh",
        "Coût unitaire (Dh)": f"{st.session_state.cout_unitaire[produit]:.2f} Dh",
        "Marge unitaire (Dh)": f"{marge_unitaire:.2f} Dh",
        "Commandes/jour": st.session_state.commandes_jour[produit],
        "Revenu mensuel (Dh)": f"{revenu_mensuel:.2f} Dh",
        "Coût mensuel (Dh)": f"{cout_mensuel:.2f} Dh",
        "Marge mensuelle (Dh)": f"{marge_mensuelle:.2f} Dh"
    })

# Ajouter une ligne de total
total_commands = sum(st.session_state.commandes_jour.values())
total_revenue = sum(indicateurs['revenus_produits'].values())
total_costs = sum(indicateurs['couts_produits'].values())
total_margins = sum(indicateurs['marges_produits'].values())

produits_data_updated.append({
    "Produit": "📊 TOTAL",
    "Prix unitaire (Dh)": "-",
    "Coût unitaire (Dh)": "-",
    "Marge unitaire (Dh)": "-",
    "Commandes/jour": total_commands,
    "Revenu mensuel (Dh)": f"{total_revenue:.2f} Dh",
    "Coût mensuel (Dh)": f"{total_costs:.2f} Dh",
    "Marge mensuelle (Dh)": f"{total_margins:.2f} Dh"
})

df_produits_updated = pd.DataFrame(produits_data_updated)
st.dataframe(df_produits_updated, use_container_width=True)

# 5. Tableau des charges mensuelles (éditable)
st.markdown('<p class="sub-header">💸 Détail des charges mensuelles</p>', unsafe_allow_html=True)

with st.form(key="charges_form"):
    # Table éditable pour les charges
    charges_data = []
    
    # Utiliser des colonnes pour organiser les champs de formulaire
    col1, col2 = st.columns(2)
    charges_keys = list(st.session_state.charges_mensuelles.keys())
    
    half = len(charges_keys) // 2 + len(charges_keys) % 2
    
    with col1:
        for i, charge in enumerate(charges_keys[:half]):
            emoji = charges_emojis.get(charge, "📝")
            montant = st.number_input(
                f"{emoji} {charge} (Dh)",
                min_value=0.0,
                value=st.session_state.charges_mensuelles[charge],
                step=10.0,
                format="%.2f",
                key=f"charge_{i}"
            )
            st.session_state.charges_mensuelles[charge] = montant
            charges_data.append({
                "Charge": f"{emoji} {charge}",
                "Montant (Dh)": f"{montant:.2f} Dh"
            })
    
    with col2:
        for i, charge in enumerate(charges_keys[half:]):
            emoji = charges_emojis.get(charge, "📝")
            montant = st.number_input(
                f"{emoji} {charge} (Dh)",
                min_value=0.0,
                value=st.session_state.charges_mensuelles[charge],
                step=10.0,
                format="%.2f",
                key=f"charge_{i + half}"
            )
            st.session_state.charges_mensuelles[charge] = montant
            charges_data.append({
                "Charge": f"{emoji} {charge}",
                "Montant (Dh)": f"{montant:.2f} Dh"
            })
    
    # Bouton pour soumettre les modifications
    charges_submitted = st.form_submit_button("Mettre à jour les charges")
    if charges_submitted:
        st.success("Charges mises à jour! Les calculs ont été recalculés.")
        indicateurs = calculer_indicateurs()  # Recalculer les indicateurs

# Ajouter une ligne de total pour les charges
total_charges = sum(st.session_state.charges_mensuelles.values())
charges_data.append({
    "Charge": "📊 TOTAL",
    "Montant (Dh)": f"{total_charges:.2f} Dh"
})

df_charges = pd.DataFrame(charges_data)
st.dataframe(df_charges, use_container_width=True)

# 6. Tableau des charges d'investissement (éditable)
st.markdown('<p class="sub-header">🏗️ Charges d\'investissement</p>', unsafe_allow_html=True)

# Regroupement des investissements par catégorie pour une meilleure organisation
investissements_categories = {
    "Équipements": [
        "Crépier", "Gauffrel", "Plaque & Pancakes", "Blender", "Extracteur de jus",
        "Machine café", "Vitrine 2 glaces", "Réfrigérateur", "Congélateur",
        "Presse agrume", "Ustensiles", "Produits initiales"
    ],
    "Aménagement": [
        "Peinture & Travaux", "Décoration & Lumières", "Étagères", "Comptoir",
        "Tables + Chaises", "Panneaux extérieurs", "TV + Caisse enregistreuse",
        "Caméras de surveillance"
    ],
    "Divers": ["Loyer avance", "Publicités"]
}

with st.form(key="investissements_form"):
    for categorie, items in investissements_categories.items():
        st.markdown(f"#### {categorie}")
        
        # Utiliser des colonnes pour organiser les champs
        cols = st.columns(2)
        half = len(items) // 2 + len(items) % 2
        
        for i, item in enumerate(items[:half]):
            with cols[0]:
                montant = st.number_input(
                    f"{item}",
                    min_value=0.0,
                    value=st.session_state.charges_investissement.get(item, 0.0),
                    step=100.0,
                    format="%.2f",
                    key=f"inv_{categorie}_{i}"
                )
                st.session_state.charges_investissement[item] = montant
        
        for i, item in enumerate(items[half:]):
            with cols[1]:
                montant = st.number_input(
                    f"{item}",
                    min_value=0.0,
                    value=st.session_state.charges_investissement.get(item, 0.0),
                    step=100.0,
                    format="%.2f",
                    key=f"inv_{categorie}_{i + half}"
                )
                st.session_state.charges_investissement[item] = montant
        
        st.markdown("---")
    
    # Bouton pour soumettre les modifications
    inv_submitted = st.form_submit_button("Mettre à jour les investissements")
    if inv_submitted:
        st.success("Investissements mis à jour! Les calculs ont été recalculés.")
        indicateurs = calculer_indicateurs()  # Recalculer les indicateurs

# Afficher le tableau des investissements
inv_data = []
for categorie, items in investissements_categories.items():
    for item in items:
        inv_data.append({
            "Catégorie": categorie,
            "Investissement": item,
            "Montant (Dh)": f"{st.session_state.charges_investissement.get(item, 0.0):.2f} Dh"
        })

# Ajouter une ligne de total pour les investissements
total_inv = sum(st.session_state.charges_investissement.values())
inv_data.append({
    "Catégorie": "",
    "Investissement": "📊 TOTAL",
    "Montant (Dh)": f"{total_inv:.2f} Dh"
})

df_inv = pd.DataFrame(inv_data)
st.dataframe(df_inv, use_container_width=True)

# 7. Graphiques en camembert pour la répartition des coûts
st.markdown('<p class="sub-header">📉 Répartition des coûts</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Camembert des coûts variables par produit
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    labels_produits = [f"{st.session_state.produits[produit]} {produit}" for produit in st.session_state.produits]
    valeurs = [indicateurs['couts_produits'][produit] for produit in st.session_state.produits]
    
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
    labels_charges = [f"{charges_emojis.get(charge, '📝')} {charge}" for charge in st.session_state.charges_mensuelles]
    valeurs_charges = [st.session_state.charges_mensuelles[charge] for charge in st.session_state.charges_mensuelles]
    
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

# 8. Analyse de rentabilité
st.markdown('<p class="sub-header">📈 Analyse de rentabilité</p>', unsafe_allow_html=True)

# Utilisation de colonnes pour une meilleure organisation
col1, col2 = st.columns(2)

with col1:
    # Calcul du point mort (seuil de rentabilité)
    if indicateurs['revenu_brut'] > 0:
        st.metric(label="Seuil de rentabilité mensuel", value=f"{indicateurs['seuil_rentabilite']:.2f} Dh")
        st.metric(label="Marge sur coût variable", value=f"{indicateurs['marge_cout_variable']:.2f}%")

with col2:
    # Calcul du ROI
    if indicateurs['total_investissement'] > 0:
        st.metric(label="ROI mensuel", value=f"{indicateurs['roi_mensuel']:.2f}%")
        st.metric(label="ROI annuel", value=f"{indicateurs['roi_annuel']:.2f}%")
        
        if indicateurs['profit_net'] > 0:
            st.metric(label="Temps de retour sur investissement",
                     value=f"{indicateurs['temps_retour']:.1f} mois ({indicateurs['temps_retour']/12:.1f} ans)")
        else:
            st.warning("Le profit net est négatif ou nul, impossible de calculer le temps de retour sur investissement.")
    else:
        st.warning("Veuillez définir des charges d'investissement pour calculer le ROI.")

# 9. Affichage d'un rapport final et des recommandations
st.markdown('<p class="sub-header">🔍 Rapport final et recommandations</p>', unsafe_allow_html=True)

if indicateurs['profit_net'] > 0:
    st.success("✅ **Votre projet est rentable!**")
    
    # Calcul des produits les plus rentables
    marges_produits_list = [(p, indicateurs['marges_produits'][p]) for p in st.session_state.produits]
    marges_produits_list.sort(key=lambda x: x[1], reverse=True)
    
    st.markdown("### 🏆 Produits les plus rentables:")
    for i, (produit, marge) in enumerate(marges_produits_list[:3]):
        if marge > 0:
            st.markdown(f"{i+1}. **{st.session_state.produits[produit]} {produit}** - Marge mensuelle: {marge:.2f} Dh")
    
    # Recommendations plus détaillées
    st.markdown("### 💡 Recommandations:")
    
    # Colonnes pour une présentation plus attrayante
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        #### Pour augmenter votre rentabilité:
        - Augmentez les prix des produits à forte demande
        - Concentrez vos efforts sur les produits les plus rentables
        - Optimisez votre approvisionnement pour réduire les coûts variables
        - Envisagez d'ajouter des produits complémentaires à forte marge
        """)
    
    with rec_col2:
        st.markdown("""
        #### Pour une croissance durable:
        - Mettez en place un système de suivi des coûts et des ventes
        - Envisagez une expansion progressive après la période de retour sur investissement
        - Développez des stratégies marketing pour augmenter le volume des ventes
        - Surveillez régulièrement les indicateurs de performance
        """)
    
    # Calculer les produits qui pourraient bénéficier d'une augmentation de prix
    prix_augmentation = []
    for produit in st.session_state.produits:
        if st.session_state.prix_vente[produit] < 3 * st.session_state.cout_unitaire[produit]:
            prix_augmentation.append(produit)
    
    if prix_augmentation:
        st.markdown("#### Produits dont vous pourriez augmenter les prix:")
        for produit in prix_augmentation:
            st.markdown(f"- {st.session_state.produits[produit]} **{produit}**: Prix actuel {st.session_state.prix_vente[produit]:.2f} Dh, prix suggéré: {st.session_state.cout_unitaire[produit] * 3:.2f} Dh")
else:
    st.error("⚠️ **Votre projet n'est pas rentable dans sa configuration actuelle.**")
    
    # Analyser les causes possibles
    problemes = []
    if indicateurs['revenu_brut'] < indicateurs['cout_fixe']:
        problemes.append("Les revenus sont insuffisants pour couvrir les charges fixes")
    
    if indicateurs['marge_cout_variable'] < 40:
        problemes.append("La marge sur coût variable est trop faible")
    
    produits_non_rentables = []
    for produit in st.session_state.produits:
        if indicateurs['marges_produits'][produit] < 0:
            produits_non_rentables.append(produit)
    
    if produits_non_rentables:
        problemes.append(f"Certains produits ne sont pas rentables: {', '.join(produits_non_rentables)}")
    
    st.markdown("### 🔍 Analyse des problèmes:")
    for i, probleme in enumerate(problemes):
        st.markdown(f"{i+1}. **{probleme}**")
    
    st.markdown("### 💡 Recommandations:")
    st.markdown("""
    - Augmentez les prix de vente ou le volume des ventes
    - Réduisez les coûts fixes ou les coûts variables
    - Concentrez-vous sur les produits à plus forte marge
    - Réévaluez les investissements initiaux
    - Envisagez de retirer ou de reformuler les produits non rentables
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>SimuProfit 2.0 - Votre outil de planification financière pour votre commerce alimentaire</p>
</div>
""", unsafe_allow_html=True)

# Bouton pour télécharger un rapport PDF (simulation)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.download_button(
        label="📊 Télécharger le rapport PDF",
        data="Cette fonctionnalité n'est pas encore disponible dans cette version.",
        file_name="simulateur_rapport.txt",
        mime="text/plain",
    )

# Ajout de conseils supplémentaires (optionnel)
with st.expander("Conseils pour améliorer votre rentabilité"):
    st.markdown("""
    #### Stratégies pour augmenter votre chiffre d'affaires:
    1. **Heures d'ouverture optimisées**: Analysez les heures de pointe et ajustez vos horaires.
    2. **Promotions ciblées**: Créez des offres spéciales pour les produits à forte marge.
    3. **Fidélisation clients**: Mettez en place un programme de fidélité.
    4. **Marketing digital**: Utilisez les réseaux sociaux pour promouvoir votre commerce.
    
    #### Comment réduire vos coûts:
    1. **Négociez avec vos fournisseurs**: Des achats en plus grande quantité peuvent réduire les prix unitaires.
    2. **Optimisez votre menu**: Concentrez-vous sur les produits rentables et retirez ceux qui ne le sont pas.
    3. **Réduisez le gaspillage**: Améliorez la gestion des stocks et la conservation des produits.
    4. **Optimisez la consommation d'énergie**: Utilisez des appareils économes en énergie.
    """)
