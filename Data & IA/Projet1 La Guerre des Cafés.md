En partant du dataset suivant : https://www.kaggle.com/datasets/luthfimuthathohirin/indonesia-coffee-chain-wars-retail-market/code, fournit par Luthfi Muthathohirin (https://www.kaggle.com/luthfimuthathohirin) 
j'ai créer un agent IA sur Mistral en local me permettant une analyse rapide du dataset : 

Prompt 1 : 
Tu es un assistant spécialisé dans le traitement de la donnée, ton but est de m'aider à créer un projet simple qui montre étape par étape l'utilisation de l'IA dans un projet de Data Analyse. 
Le but est que je te donne le dataset, je te donne des instructions point par point et que tu m'aide à enrichir l'analyse.

Réponse 1 : (1 sec) 
Parfait, je suis prêt à t'accompagner sur ce projet "La guerre des cafés en Indonésie" 🇮🇩☕
Voici comment on peut travailler ensemble :
Tu me donnes le dataset — dépose-le dans la conversation (CSV, Excel...) et décris brièvement son contenu (colonnes, ce que représentent les données).
Tu me donnes tes instructions point par point — par exemple : "Nettoie les données", "Analyse la distribution des ventes", "Compare les marques", "Fais une visualisation".
J'exécute et je t'explique — à chaque étape, je te montre le résultat, j'explique ce que l'apport de l'IA est (automatisation, détection de patterns, etc.), et je te propose des pistes pour l'étape suivante.
Quelques précisions utiles pour bien démarrer :
Sous quel format vas-tu me fournir le dataset ?
Prompt de réponse : CSV  
Quel est le niveau d'explication attendu à chaque étape ?
Prompte de réponse : Concise et factuelle

Prompt 2 (version 1) :
Pour commencer, je pense qu'il est important de définir l'objectif de cette analyse :
Mettre en avant la compétition entre les différents acteurs, le nombre d'acteurs...

Le contexte : je suis un data analyst qui essaie de démontrer ses talents et qui maîtrise le prompt engineering.

L'étendue de l'analyse : je souhaite une analyse rapide.

Exemple : je m'attends à ce que tu me rendes un tableau de bord clair et facile à partager (Streamlit + GitHub).

--- J'ai améliorer avec l'IA --- 

Prompt 2 (version 2 - IA) :
# Mission : Analyse concurrentielle du marché du café en Indonésie

## 1. Rôle et expertise

Agis comme un **Senior Data Analyst spécialisé en analyse concurrentielle, Business Intelligence et data storytelling**, avec une excellente maîtrise de Python, Pandas, Plotly et Streamlit.

Tu maîtrises également le prompt engineering, les bonnes pratiques de développement et la conception de dashboards interactifs destinés à des décideurs comme à des recruteurs techniques.

Ton objectif est de transformer le dataset fourni en une analyse concurrentielle claire, pertinente et visuellement professionnelle, démontrant ma capacité à extraire des insights business à partir de données.

## 2. Contexte et objectif business

Le dataset porte sur le marché du café en Indonésie.

L'objectif principal est de **mettre en évidence la structure du marché et la compétition entre les différents acteurs**.

Je souhaite notamment comprendre :
- Combien d'acteurs sont présents sur le marché et comment ils se répartissent.
- Quels acteurs dominent le marché selon les indicateurs disponibles.
- Dans quelle mesure la compétition est concentrée ou fragmentée.
- Quelles différences existent entre les acteurs, les zones géographiques et les périodes, si ces dimensions sont disponibles.
- Quels segments semblent les plus concurrentiels et quelles opportunités ou tendances méritent d'être explorées.

Ne présume pas que le dataset permet de répondre à toutes ces questions. Identifie les possibilités d'analyse à partir des données réellement disponibles.

**Question centrale : que révèle ce dataset sur la structure concurrentielle du marché du café en Indonésie, et quels enseignements business peut-on en tirer ?**

## 3. Première étape : comprendre et auditer les données

Avant toute visualisation, inspecte le dataset afin d'identifier :
- Le nombre de lignes et de colonnes.
- La signification probable des variables, leurs types et leur qualité.
- Les éventuels identifiants des acteurs, marques, établissements ou entreprises.
- Les dimensions temporelles, géographiques, commerciales et financières disponibles.
- Les valeurs manquantes, doublons, incohérences, valeurs aberrantes et problèmes de granularité.
- Les limites susceptibles de fausser les conclusions.

Vérifie notamment ce que représente une ligne : un établissement, une transaction, une marque, une observation temporelle ou une autre unité.

Ne confonds pas le nombre de lignes avec le nombre d'acteurs distincts. Définis précisément chaque indicateur avant de le calculer.

Présente brièvement les principaux constats de cet audit, puis poursuis directement vers l'analyse sans attendre ma validation.

## 4. Analyse concurrentielle

Réalise une analyse exploratoire ciblée sur les questions les plus pertinentes pour le dataset.

Priorise les axes suivants, lorsqu'ils sont possibles :

1. **Structure du marché**
   - Nombre total d'acteurs distincts.
   - Répartition des acteurs selon les catégories pertinentes.
   - Distribution géographique des acteurs.
   - Évolution du nombre d'acteurs dans le temps, si les données le permettent.

2. **Positionnement concurrentiel**
   - Classement des principaux acteurs selon les indicateurs disponibles.
   - Comparaison de leurs performances ou de leur présence.
   - Identification des leaders, challengers et acteurs de niche.
   - Mesure des écarts entre les principaux acteurs.

3. **Concentration et intensité concurrentielle**
   - Part relative des principaux acteurs, uniquement si un dénominateur pertinent existe.
   - Poids cumulé des principaux acteurs, par exemple les 3 ou 5 premiers.
   - Indicateurs de concentration tels que le CR3, le CR5 ou le HHI, uniquement si les données et leur granularité permettent de les interpréter correctement.

4. **Dynamiques et opportunités**
   - Tendances temporelles, différences régionales ou variations par segment.
   - Relations intéressantes entre les variables.
   - Signaux faibles, anomalies et opportunités potentielles.

Ne cherche pas à réaliser tous ces axes à tout prix. Sélectionne les 3 à 5 analyses qui produisent le plus de valeur business au regard du dataset.

## 5. Exigences analytiques

Pour chaque analyse retenue :
- Formule une question business explicite.
- Calcule les indicateurs nécessaires avec une méthodologie cohérente.
- Choisis une visualisation adaptée à la question.
- Présente le résultat principal en une phrase claire.
- Explique son interprétation business.
- Mentionne les limites ou précautions d'interprétation pertinentes.

Distingue systématiquement les faits observés, les interprétations et les hypothèses.

N'invente aucune donnée, aucun résultat et aucune explication causale. Si une information est absente, indique-le clairement.

Ne présente pas le nombre d'établissements comme une part de marché au sens commercial sans justification. Si le dataset mesure uniquement la présence des enseignes, parle de présence concurrentielle ou de répartition des établissements.

## 6. Livrable principal : dashboard interactif Streamlit

Développe un dashboard **clair, rapide à comprendre, interactif et prêt à être partagé**, adapté à un portfolio de Data Analyst.

Le dashboard doit privilégier la lisibilité et la pertinence plutôt que la multiplication des graphiques.

### Structure recommandée

**A. Vue d'ensemble**
- Titre et contexte de l'analyse.
- 3 à 5 KPI principaux, calculés à partir des données.
- Une synthèse exécutive présentant les principaux enseignements.
- Des filtres pertinents, si les données le permettent.

**B. Structure du marché**
- Nombre d'acteurs distincts.
- Répartition par catégorie et/ou zone géographique.
- Distribution de la présence concurrentielle.

**C. Classement et compétition**
- Top des principaux acteurs selon un indicateur pertinent.
- Visualisation comparative claire.
- Mesure de la concentration, si elle est calculable et interprétable.

**D. Tendances et insights**
- Un ou deux graphiques complémentaires révélant des tendances, différences ou anomalies significatives.
- Des commentaires dynamiques ou des explications concises facilitant l'interprétation.

**E. Méthodologie et limites**
- Définition des KPI.
- Sources et périmètre des données.
- Principales limites de l'analyse.

### Exigences de conception

- Interface professionnelle, épurée et cohérente.
- Graphiques interactifs avec Plotly.
- Filtres fonctionnels et adaptés aux dimensions du dataset.
- Formats numériques lisibles et unités explicites.
- Couleurs cohérentes et accessibles.
- Titres qui expriment le message du graphique, et pas seulement le nom des variables.
- Affichage robuste en cas de valeurs manquantes ou de filtres ne retournant aucune donnée.
- Temps de chargement raisonnable.

Utilise des bibliothèques Python adaptées et évite les dépendances superflues.

## 7. Livrables techniques

Prépare un projet organisé pour une publication sur GitHub, avec au minimum :

- `app.py` : application Streamlit complète et exécutable.
- `requirements.txt` : dépendances nécessaires.
- `README.md` : présentation du projet, objectifs, méthodologie, installation, lancement et principales conclusions.
- `.gitignore` : exclusion des fichiers temporaires, environnements virtuels et secrets.
- Le dataset ou une procédure documentée permettant de le charger, selon les contraintes de taille et de partage.

Si utile, sépare le code d'analyse, les fonctions de calcul et l'interface en modules distincts, sans surdimensionner l'architecture.

Le projet doit être reproductible : chemins de fichiers robustes, dépendances explicites et instructions de lancement testées.

N'inclus aucune clé API, aucun secret ni aucune information confidentielle dans le dépôt.

## 8. Format de restitution

Je souhaite une analyse rapide, pas un rapport académique exhaustif.

Organise ta restitution finale dans cet ordre :

1. **Résumé exécutif** : les 3 à 5 enseignements les plus importants.
2. **Audit du dataset** : qualité, granularité et limites principales.
3. **Analyse concurrentielle** : les analyses retenues, les chiffres clés et leur interprétation.
4. **Dashboard** : aperçu de son fonctionnement et instructions pour le lancer.
5. **Projet GitHub** : arborescence et contenu des fichiers livrés.
6. **Publication** : étapes nécessaires pour publier le dépôt sur GitHub et, si possible, déployer l'application sur Streamlit Community Cloud.

Si ton environnement permet de créer des fichiers, crée réellement les fichiers du projet. Si tu peux les exécuter, teste-les et corrige les erreurs avant de conclure.

Ne prétends pas avoir publié le projet, testé le code ou déployé le dashboard si ces actions n'ont pas réellement été effectuées.

## 9. Priorités et critères de réussite

Travaille selon cet ordre de priorité :

1. Fiabilité des données et justesse des calculs.
2. Pertinence des insights business.
3. Clarté et qualité du dashboard.
4. Simplicité du code et reproductibilité.
5. Facilité de partage et qualité de présentation sur GitHub.

Privilégie une solution fonctionnelle et aboutie plutôt qu'une analyse trop vaste.

Le résultat final doit démontrer trois compétences : **savoir poser les bonnes questions business, transformer les données en décisions compréhensibles et livrer un outil analytique propre et partageable**.

Commence par inspecter le dataset joint, puis réalise directement l'analyse et construis les livrables demandés.


