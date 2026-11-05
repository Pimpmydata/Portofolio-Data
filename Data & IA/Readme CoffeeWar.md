☕ La guerre des cafés en Indonésie — Analyse concurrentielle

Projet portfolio de Data Analyst : analyse concurrentielle du marché du café en Indonésie à partir d'un dataset enrichi 2026, livrée sous forme de dashboard Streamlit interactif.

🎯 Objectif business

Mettre en évidence la structure concurrentielle du marché : combien d'acteurs, qui domine, à quel point le marché est concentré, et quelles dynamiques (guerre des prix, vouchers, cannibalisation) méritent l'attention d'un décideur.

📊 Questions posées

Structure : combien de marques et de points de vente, et comment se répartissent-ils par zone et par format ?

Hiérarchie : qui sont le leader, les challengers et les acteurs de niche selon le CA journalier estimé ?

Concentration : CR3, CR5 et HHI — le marché est-il fragmenté ou dominé par quelques acteurs ?

Dynamiques : la guerre des vouchers (remises élevées) génère-t-elle du volume, et à quel coût sur la marge ?

🧠 Méthodologie en une minute

Granularité : une ligne = un point de vente (store_transaction_id unique) avec des estimés journaliers (ventes, CA, marge).

Part de CA estimé : part relative au sein de l'échantillon — pas une part de marché nationale.

Présence concurrentielle : nombre de points de vente, toujours présentée distinctement de la performance économique.

HHI : somme des parts² × 10 000 ; seuils usuels 1 500 / 2 500 (lignes directrices antitrust US).

La colonne texte volumineuse (cot_retail_dynamics_rationale) est exclue du chargement pour la performance.

🚀 Installation et lancement

# 1. Cloner le dépôt
git clone https://github.com/<ton-user>/coffee-wars-indonesia.git
cd coffee-wars-indonesia

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Placer le dataset dans le dossier data/
#    (indonesia_coffee_chain_wars_enriched_2026.csv)

# 5. Lancer le dashboard
streamlit run coffee_war.py

L'application s'ouvre sur http://localhost:8501.

📁 Arborescence du projet

coffee-wars-indonesia/
├── coffee_war.py             # Application Streamlit complète (audit + KPI + graphiques Plotly)
├── requirements.txt     # Dépendances
├── README.md            # Ce fichier
├── .gitignore           # Exclusions Git
└── data/
    └── indonesia_coffee_chain_wars_enriched_2026.csv   # Dataset (voir note ci-dessous)

📄 Autres fichiers du projet

requirements.txt

streamlit>=1.35
pandas>=2.0
plotly>=5.20
numpy>=1.26

.gitignore

.venv/
venv/
__pycache__/
*.pyc
.DS_Store
.streamlit/secrets.toml
.env

Note dataset : si le fichier CSV est trop volumineux pour GitHub (> 100 Mo), utilise Git LFS ou documente un lien de téléchargement dans le README (Google Drive, Kaggle, etc.) sans inclure le fichier au dépôt.

🖥️ Le dashboard

Cinq onglets, des filtres marque / ville / format dans la barre latérale :

Onglet

Contenu

Vue d'ensemble

5 KPI + synthèse exécutive dynamique + donut du CA par marque

Structure du marché

Présence par marque, CA par zone, treemap des formats

Classement & concentration

Tableau comparatif, top acteurs, CR3 / CR5 / HHI

Insights

Remises vs volume, remises vs marges, densité concurrentielle, fidélité client

Méthodologie

Définitions des KPI, audit qualité automatique, limites

⚠️ Limites principales

Pas de dimension temporelle : photographie 2026, aucune évolution mesurable.

Indicateurs estimés par le fournisseur de données (CA, marges, indices) — à considérer avec leur confidence_score.

Représentativité non garantie : agréger au niveau marque suppose que l'échantillon de points de vente est représentatif.

Corrélations ≠ causalité : les remises peuvent être ciblées sur les zones les plus concurrentielles.

🔍 Principales conclusions

(Les chiffres exacts sont calculés dynamiquement par le dashboard sur ton dataset ; en l'état de l'échantillon exploré :)

Le marché est structuré autour de chaînes de café indonésiennes en concurrence prix : remises voucher agressives (souvent 15–40 %) et positionnements différenciés par segment client (Gen Z, travailleurs, familles, pendulaires).

La fidélité client est fragile : une part significative des points de vente s'adresse à des Promo-Chasers, sensibles à l'ouverture d'un concurrent moins cher.

Le principal moteur de switch observé dans les données est l'ouverture d'un concurrent moins cher dans un rayon de 500 m — la densité locale, pas seulement le prix global, structure la compétition.

📦 Publier sur GitHub

git init
git add .
git commit -m "Analyse concurrentielle du marché du café en Indonésie (Streamlit)"
git branch -M main
git remote add origin https://github.com/<ton-user>/coffee-wars-indonesia.git
git push -u origin main

☁️ Déployer sur Streamlit Community Cloud

Pousse le dépôt sur GitHub (dataset via LFS ou lien documenté).

Va sur share.streamlit.io et connecte ton compte GitHub.

New app → sélectionne le dépôt, la branche main, le fichier coffee_war.py.

Clique Deploy — l'app est servie sur une URL publique en quelques minutes.

🛠️ Stack

Python 3.10+ · Streamlit · Pandas · Plotly
