import glob
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration générale
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="☕ Guerre des cafés en Indonésie",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETTE = ["#6F4E37", "#A9744F", "#C89F84", "#8B5E3C", "#D2B48C", "#4E342E", "#B08968", "#7F5539"]

NUMERIC_COLS = [
    "competitor_density_500m", "base_price_idr", "discount_voucher_pct",
    "daily_cups_sold", "customer_review_rating", "dwell_time_minutes",
    "net_discounted_price_idr", "daily_revenue_estimate_idr",
    "price_competitiveness_ratio", "cannibalization_risk_index",
    "customer_price_sensitivity_score", "outlet_operating_margin_estimate_pct",
    "confidence_score",
]
CATEGORICAL_COLS = [
    "coffee_brand", "city_location", "store_format", "order_method",
    "coffee_beans_type", "store_amenities", "primary_customer_segment",
    "customer_brand_loyalty_tier", "primary_brand_switch_driver",
]
# Colonne ignorée volontairement : cot_retail_dynamics_rationale (texte libre très volumineux,
# sans valeur pour les agrégats ; on l'exclut pour garder le chargement rapide).
USE_COLS = ["store_transaction_id"] + NUMERIC_COLS + CATEGORICAL_COLS


# ---------------------------------------------------------------------------
# Chargement des données
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Charge le CSV depuis data/ ou la racine du projet."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = (
        glob.glob(os.path.join(here, "data", "*.csv"))
        + glob.glob(os.path.join(here, "*.csv"))
    )
    if not candidates:
        st.error(
            "Aucun fichier CSV trouvé. Place le dataset dans le dossier `data/` "
            "ou à la racine du projet, puis relance l'application."
        )
        st.stop()

    path = max(candidates, key=os.path.getsize)  # le plus gros CSV = le dataset
    df = pd.read_csv(path, usecols=lambda c: c in USE_COLS, low_memory=False)
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in CATEGORICAL_COLS:
        if c in df.columns:
            df[c] = df[c].fillna("Non renseigné").astype(str)
    return df


def fmt_idr(v: float) -> str:
    """Formate un montant en Roupies indonésiennes de façon lisible."""
    if pd.isna(v):
        return "n/a"
    if abs(v) >= 1_000_000_000:
        return f"{v / 1_000_000_000:.1f} Mds Rp"
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.1f} M Rp"
    return f"{v:,.0f} Rp".replace(",", " ")


def concentration(shares: pd.Series) -> dict:
    """CR3, CR5 et HHI à partir d'une série de parts (0-1)."""
    s = shares.dropna().sort_values(ascending=False)
    if s.empty:
        return {}
    return {
        "CR3": s.head(3).sum(),
        "CR5": s.head(5).sum(),
        "HHI": float((s ** 2).sum() * 10_000),
    }


# ---------------------------------------------------------------------------
# Données + filtres
# ---------------------------------------------------------------------------
raw = load_data()
df_all = raw.drop_duplicates(subset=["store_transaction_id"], keep="first").copy()

st.sidebar.title("☕ Guerre des cafés")
st.sidebar.caption("Analyse concurrentielle du marché du café en Indonésie — 2026")

st.sidebar.subheader("Filtres")
brands = st.sidebar.multiselect(
    "Marques", sorted(df_all["coffee_brand"].unique()),
    default=sorted(df_all["coffee_brand"].unique()),
)
cities = st.sidebar.multiselect(
    "Villes", sorted(df_all["city_location"].unique()),
    default=sorted(df_all["city_location"].unique()),
)
formats_ = st.sidebar.multiselect(
    "Formats de point de vente", sorted(df_all["store_format"].unique()),
    default=sorted(df_all["store_format"].unique()),
)

df = df_all[
    df_all["coffee_brand"].isin(brands)
    & df_all["city_location"].isin(cities)
    & df_all["store_format"].isin(formats_)
].copy()

if df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés. Élargis ta sélection dans la barre latérale.")
    st.stop()

# ---------------------------------------------------------------------------
# Vue d'ensemble
# ---------------------------------------------------------------------------
tab_overview, tab_structure, tab_ranking, tab_insights, tab_method = st.tabs(
    ["Vue d'ensemble", "Structure du marché", "Classement & concentration", "Insights", "Méthodologie"]
)

with tab_overview:
    st.title("☕ La guerre des cafés en Indonésie")
    st.caption("Structure concurrentielle du marché — analyse par point de vente, indicateurs estimés 2026.")

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Points de vente", f"{len(df):,}".replace(",", " "))
    kpi2.metric("Marques distinctes", df["coffee_brand"].nunique())
    kpi3.metric("Villes couvertes", df["city_location"].nunique())
    kpi4.metric("Tasses / jour (éch. filtré)", f"{df['daily_cups_sold'].sum():,.0f}".replace(",", " "))
    kpi5.metric("CA journalier estimé", fmt_idr(df["daily_revenue_estimate_idr"].sum()))

    st.subheader("Synthèse exécutive")
    by_revenue = (
        df.groupby("coffee_brand")["daily_revenue_estimate_idr"].sum()
        .sort_values(ascending=False)
    )
    leader = by_revenue.index[0]
    conc = concentration(by_revenue / by_revenue.sum())
    top3 = ", ".join(by_revenue.head(3).index.tolist())
    avg_disc = df["discount_voucher_pct"].mean()
    hhi_txt = f"{conc.get('HHI', 0):,.0f}".replace(",", " ")
    structure_txt = (
        "marché concentré" if conc.get("HHI", 0) > 2500
        else ("concentration modérée" if conc.get("HHI", 0) > 1500 else "marché fragmenté")
    )
    st.markdown(
        f"""
        - **Leader estimé** : **{leader}** concentre la plus grosse part de CA journalier estimé
          sur le périmètre filtré ({by_revenue.iloc[0] / by_revenue.sum():.0%}).
        - **Top 3** ({top3}) cumulent **{conc.get('CR3', 0):.0%}** du CA journalier estimé.
        - **Concentration** : HHI ≈ **{hhi_txt}** → {structure_txt}.
        - **Arme compétitive dominante** : remise moyenne de **{avg_disc:.1f}%** par voucher,
          signe d'une concurrence prix forte.
        """
    )

    st.subheader("Répartition du CA journalier estimé par marque")
    fig = px.pie(
        values=by_revenue.values, names=by_revenue.index,
        hole=0.45, color_discrete_sequence=PALETTE,
    )
    fig.update_traces(textinfo="percent+label", textposition="outside")
    fig.update_layout(margin=dict(t=30, b=30), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Structure du marché
# ---------------------------------------------------------------------------
with tab_structure:
    st.subheader("Combien d'acteurs, et où sont-ils ?")
    st.caption(
        "⚠️ Chaque ligne du dataset = **un point de vente** (pas une transaction ni une marque). "
        "On mesure donc la **présence concurrentielle** (nombre de points de vente), pas une part de marché réelle."
    )

    c1, c2 = st.columns(2)
    with c1:
        presence = (
            df.groupby("coffee_brand")["store_transaction_id"].count()
            .sort_values(ascending=True)
        )
        fig = px.bar(
            x=presence.values, y=presence.index, orientation="h",
            labels={"x": "Points de vente", "y": ""},
            color_discrete_sequence=[PALETTE[0]],
            title="Présence concurrentielle : points de vente par marque",
        )
        fig.update_layout(margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        by_city = (
            df.groupby("city_location")["daily_revenue_estimate_idr"].sum()
            .sort_values(ascending=True)
        )
        fig = px.bar(
            x=by_city.values, y=by_city.index, orientation="h",
            labels={"x": "CA journalier estimé (Rp)", "y": ""},
            color_discrete_sequence=[PALETTE[2]],
            title="CA journalier estimé par zone géographique",
        )
        fig.update_layout(margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Répartition par format de point de vente")
    fmt = df.groupby("store_format").agg(
        points=("store_transaction_id", "count"),
        ca=("daily_revenue_estimate_idr", "sum"),
        tasses=("daily_cups_sold", "sum"),
    ).sort_values("points", ascending=False)
    fig = px.treemap(
        fmt.reset_index(), path=["store_format"], values="points",
        color="ca", color_continuous_scale="Brwnyl",
        title="Points de vente par format (couleur = CA journalier estimé)",
    )
    fig.update_layout(margin=dict(t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Classement & concentration
# ---------------------------------------------------------------------------
with tab_ranking:
    st.subheader("Qui domine le marché ?")
    ranking = (
        df.groupby("coffee_brand")
        .agg(
            points=("store_transaction_id", "count"),
            ca_journalier=("daily_revenue_estimate_idr", "sum"),
            tasses_jour=("daily_cups_sold", "sum"),
            prix_net_moyen=("net_discounted_price_idr", "mean"),
            remise_moyenne=("discount_voucher_pct", "mean"),
            note_moyenne=("customer_review_rating", "mean"),
            marge_moyenne=("outlet_operating_margin_estimate_pct", "mean"),
        )
        .sort_values("ca_journalier", ascending=False)
    )
    ranking["part_ca"] = ranking["ca_journalier"] / ranking["ca_journalier"].sum()

    st.dataframe(
        ranking.style.format({
            "ca_journalier": "{:,.0f}",
            "tasses_jour": "{:,.0f}",
            "prix_net_moyen": "{:,.0f}",
            "remise_moyenne": "{:.1f}",
            "note_moyenne": "{:.2f}",
            "marge_moyenne": "{:.1f}",
            "part_ca": "{:.1%}",
        }),
        use_container_width=True,
    )

    st.subheader("Classement par CA journalier estimé")
    fig = px.bar(
        ranking.reset_index().sort_values("ca_journalier", ascending=True),
        x="ca_journalier", y="coffee_brand", orientation="h",
        labels={"ca_journalier": "CA journalier estimé (Rp)", "coffee_brand": ""},
        color="note_moyenne", color_continuous_scale="Brwnyl",
        title="Leader vs challengers (couleur = note client moyenne)",
    )
    fig.update_layout(margin=dict(t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Concentration du marché")
    rev_shares = ranking["part_ca"]
    pres_shares = ranking["points"] / ranking["points"].sum()
    conc_rev = concentration(rev_shares)
    conc_pres = concentration(pres_shares)

    c1, c2, c3 = st.columns(3)
    c1.metric("CR3 (CA estimé)", f"{conc_rev['CR3']:.0%}")
    c2.metric("CR5 (CA estimé)", f"{conc_rev['CR5']:.0%}")
    hhi = conc_rev["HHI"]
    c3.metric(
        "HHI (CA estimé)", hhi_txt,
        help="Somme des parts² × 10 000. Seuils usuels : > 2 500 = marché concentré, 1 500–2 500 = modérément concentré.",
    )

    st.caption(
        f"À titre de comparaison, sur la seule présence (nb de points de vente) : "
        f"CR3 = {conc_pres['CR3']:.0%}, HHI = {conc_pres['HHI']:,.0f}".replace(",", " ")
        + ". Les seuils HHI usuels (1 500 / 2 500) proviennent des lignes directrices antitrust américaines."
    )

    st.subheader("Écarts entre leaders et challengers")
    if len(ranking) >= 2:
        gap = ranking["ca_journalier"].iloc[0] / ranking["ca_journalier"].iloc[1]
        st.markdown(
            f"- Le n°1 génère **{gap:.1f}×** le CA journalier estimé du n°2."
            f"- Écart de présence : {ranking['points'].iloc[0]} vs {ranking['points'].iloc[1]} points de vente."
        )

# ---------------------------------------------------------------------------
# Insights
# ---------------------------------------------------------------------------
with tab_insights:
    st.subheader("Remises vs volume : la guerre des vouchers est-elle efficace ?")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            df, x="discount_voucher_pct", y="daily_cups_sold",
            color="coffee_brand", color_discrete_sequence=PALETTE,
            labels={"discount_voucher_pct": "Remise voucher (%)", "daily_cups_sold": "Tasses vendues / jour"},
            title="Des remises plus élevées ne garantissent pas plus de volume",
            hover_data=["city_location", "store_format"],
        )
        fig.update_layout(margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(
            df, x="discount_voucher_pct", y="outlet_operating_margin_estimate_pct",
            color="coffee_brand", color_discrete_sequence=PALETTE,
            labels={
                "discount_voucher_pct": "Remise voucher (%)",
                "outlet_operating_margin_estimate_pct": "Marge opérationnelle estimée (%)",
            },
            title="Le prix de la guerre des prix : remise vs marge",
            hover_data=["city_location", "store_format"],
        )
        fig.update_layout(margin=dict(t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    corr = df[["discount_voucher_pct", "daily_cups_sold", "outlet_operating_margin_estimate_pct"]].corr()
    st.markdown(
        f"""
        **Lecture** : corrélation remise → volume : **{corr.loc['discount_voucher_pct', 'daily_cups_sold']:+.2f}** ;
        remise → marge : **{corr.loc['discount_voucher_pct', 'outlet_operating_margin_estimate_pct']:+.2f}**.
        Une corrélation n'est pas une causalité : les remises peuvent être ciblées sur les zones les plus concurrentielles.
        """
    )

    st.subheader("Intensité concurrentielle locale et cannibalisation")
    fig = px.box(
        df.sort_values("coffee_brand"),
        x="coffee_brand", y="competitor_density_500m", color="coffee_brand",
        color_discrete_sequence=PALETTE,
        labels={"competitor_density_500m": "Compétiteurs dans un rayon de 500 m", "coffee_brand": ""},
        title="Densité concurrentielle subie par chaque marque",
    )
    fig.update_layout(showlegend=False, margin=dict(t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Profils de fidélité client par marque")
    loyalty = (
        df.groupby(["coffee_brand", "customer_brand_loyalty_tier"])["store_transaction_id"]
        .count().reset_index(name="points")
    )
    fig = px.bar(
        loyalty, x="coffee_brand", y="points", color="customer_brand_loyalty_tier",
        color_discrete_sequence=PALETTE,
        labels={"points": "Points de vente", "customer_brand_loyalty_tier": "Profil de fidélité"},
        title="Fidélité client : Promo-Chasers vs Die-Hard Loyalists",
    )
    fig.update_layout(margin=dict(t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Méthodologie
# ---------------------------------------------------------------------------
with tab_method:
    st.subheader("Méthodologie et limites")
    st.markdown(
        """
        #### Définition des indicateurs
        - **Point de vente** : une ligne du dataset (`store_transaction_id` unique) décrit un point de vente,
          pas une transaction unitaire. Les colonnes `daily_*` sont des **estimations journalières** par point de vente.
        - **CA journalier estimé** : somme de `daily_revenue_estimate_idr` (champ fourni par le dataset, déjà estimé).
        - **Part de CA estimé** : part relative **au sein du périmètre de l'échantillon filtré** —
          ce n'est **pas** une part de marché nationale.
        - **CR3 / CR5** : part cumulée du CA journalier estimé des 3 / 5 premières marques.
        - **HHI** : somme des parts au carré × 10 000 (échelle 0–10 000). Seuils usuels : > 2 500 = concentré.
        - **Présence concurrentielle** : nombre de points de vente par marque — une mesure de présence, pas de performance.

        #### Qualité des données (audit automatique)
        """
    )
    st.markdown(
        f"""
        - Lignes brutes : **{len(raw):,}** | Doublons d'identifiant retirés : **{len(raw) - len(df_all)}**
        | Lignes après filtres : **{len(df)}**.
        - Marques : **{df_all['coffee_brand'].nunique()}** | Villes : **{df_all['city_location'].nunique()}**
        | Formats : **{df_all['store_format'].nunique()}**.
        """
    )
    missing = df_all[NUMERIC_COLS].isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        st.markdown("- Valeurs manquantes sur les colonnes numériques : **aucune** après conversion.")
    else:
        st.markdown("- Valeurs manquantes (colonnes numériques) :")
        st.dataframe(missing.rename("manquantes"), use_container_width=True)

    st.markdown(
        """
        #### Limites principales
        1. **Pas de dimension temporelle** : le dataset est une photographie (2026) ; aucune évolution dans le temps n'est mesurable.
        2. **Indicateurs estimés** : CA, marges et indices (cannibalisation, sensibilité prix) sont des estimations
           produites par le fournisseur de données, avec un `confidence_score` à considérer.
        3. **Granularité point de vente** : agréger ces estimés au niveau marque suppose que l'échantillon soit
           représentatif, ce qui n'est pas garanti.
        4. **La colonne `cot_retail_dynamics_rationale`** (texte explicatif volumineux) est exclue du chargement
           pour la performance ; elle ne contient pas de données supplémentaires exploitables pour les agrégats.
        """
    )

st.sidebar.divider()
st.sidebar.caption("Projet portfolio Data Analyst — données : dataset enrichi 2026, marché du café en Indonésie.")
