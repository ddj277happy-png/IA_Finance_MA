"""
Merge all parsed BAM data sources into a single analysis-ready CSV.

Output: data/real_estate_murabaha.csv with columns:
- date: month-end timestamp
- murabaha_immobiliere_kDH: monthly Murabaha immobilière outstanding (kDH = thousands of dirhams)
- murabaha_total_kDH: total monthly Murabaha outstanding
- murabaha_hors_marges_kDH: hors marges Murabaha totale
- murabaha_immobiliere_hors_marges_kDH
- credit_habitat_MDH: conventional Crédits à l'habitat (year-end snapshots from SM/Flash PDFs)
- credit_habitat_participatif_MDH: Financement participatif à l'habitat (from SM PDFs)
- ipai_global, ipai_residentiel, ipai_appartement: housing price indices (quarterly, forward-filled to monthly)
- policy_rate_pct: BAM key policy rate (decision dates, forward-filled)
- lending_rate_habitat_pct: Taux débiteurs Crédits immobiliers (quarterly)
- lending_rate_global_pct: Taux débiteurs Global

All time series are aligned to monthly frequency (2019-07 onwards) by forward-filling
where necessary. Quarterly data is used at its quarter month and forward-filled.
"""
import pandas as pd
import numpy as np
from pathlib import Path

INT_DIR = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/real_estate_murabaha.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)


def main():
    # 1. Monthly Murabaha (wide pivot)
    part = pd.read_csv(INT_DIR / "participatives_wide.csv", index_col=0, parse_dates=True)
    part.index.name = "date"
    part.columns = [c.strip() for c in part.columns]

    # 2. Year-end Crédits à l'habitat from SM/Flash (MDH)
    sm_flash = pd.read_csv(INT_DIR / "sm_flash_credit_series.csv", index_col=0, parse_dates=True)
    sm_flash.index.name = "date"

    # 3. Quarterly IPAI
    ipai = pd.read_csv(INT_DIR / "ipai_quarterly.csv", index_col=0, parse_dates=True)
    ipai.index.name = "date"
    ipai.columns = [c.strip() for c in ipai.columns]

    # 4. Policy rate history (decision dates)
    pol = pd.read_csv(INT_DIR / "policy_rate_history.csv", index_col=0, parse_dates=True)
    pol.index.name = "date"

    # 5. Quarterly lending rates
    taux = pd.read_csv(INT_DIR / "taux_debiteurs_quarterly.csv", index_col=0, parse_dates=True)
    taux.index.name = "date"

    # Build monthly index spanning 2019-07 to 2025-12
    monthly_idx = pd.date_range(start="2019-07-01", end="2025-12-01", freq="MS")

    df = pd.DataFrame(index=monthly_idx)
    df.index.name = "date"

    # Add Murabaha columns (rename for clarity)
    murabaha_map = {
        "Mourabaha_immobiliere": "murabaha_immobiliere_kDH",
        "Mourabaha_total": "murabaha_total_kDH",
        "Mourabaha_hors_marges_total": "murabaha_hors_marges_kDH",
        "Mourabaha_immobiliere_hors_marges": "murabaha_immobiliere_hors_marges_kDH",
        "Mourabaha_automobile": "murabaha_automobile_kDH",
        "Mourabaha_equipement": "murabaha_equipement_kDH",
        "Mourabaha_matieres_premieres": "murabaha_matieres_premieres_kDH",
        "Depot_vue": "depot_vue_kDH",
        "Depot_investissement": "depot_investissement_kDH",
    }
    for src_col, dst_col in murabaha_map.items():
        if src_col in part.columns:
            # Reindex monthly and forward-fill (to handle any month with NaN)
            s = part[src_col].reindex(monthly_idx)
            df[dst_col] = s

    # Add year-end Crédits à l'habitat from SM/Flash (forward-fill within year, keep year-end value)
    # SM gives credits_habitat_MDH (in thousands of dirhams)
    # Flash gives credits_habitat_MMDH (in millions of dirhams) — convert to MDH
    habitat_series = None
    if "credits_habitat_MDH" in sm_flash.columns:
        habitat_series = sm_flash["credits_habitat_MDH"].dropna()
    if "credits_habitat_MMDH" in sm_flash.columns:
        mmdh = sm_flash["credits_habitat_MMDH"].dropna() * 1000  # MMDH → MDH
        if habitat_series is None:
            habitat_series = mmdh
        else:
            habitat_series = habitat_series.combine_first(mmdh)

    if habitat_series is not None:
        # Reindex to monthly and forward-fill
        df["credit_habitat_MDH"] = habitat_series.reindex(monthly_idx).ffill()

    # Participatory housing credit (Financement participatif à l'habitat from SM PDFs)
    if "credits_habitat_financement_participatif_MDH" in sm_flash.columns:
        part_hab = sm_flash["credits_habitat_financement_participatif_MDH"].dropna()
        df["credit_habitat_participatif_MDH"] = part_hab.reindex(monthly_idx).ffill()

    # Also use Flash PDFs' "Mourabaha immobilière" series (in MMDH) as Murabaha immobilière cross-check
    # Note: Flash "Mourabaha immobilière" is in MMDH and represents year-end snapshot
    if "murabaha_habitat_MMDH" in sm_flash.columns:
        mb_flash = sm_flash["murabaha_habitat_MMDH"].dropna() * 1000  # MMDH → MDH
        # Forward-fill
        df["credit_habitat_participatif_flash_MDH"] = mb_flash.reindex(monthly_idx).ffill()

    # Add quarterly IPAI — forward-fill to monthly
    ipai_map = {
        "Global": "ipai_global",
        "Résidentiel": "ipai_residentiel",
        "Appartement": "ipai_appartement",
        "Maison": "ipai_maison",
    }
    for src_col, dst_col in ipai_map.items():
        if src_col in ipai.columns:
            df[dst_col] = ipai[src_col].reindex(monthly_idx).ffill()

    # Add policy rate (decision dates, resample to month-start then forward-fill)
    if "taux_directeur_pct" in pol.columns:
        pol_m = pol["taux_directeur_pct"].copy()
        pol_m.index = pol_m.index.to_period("M").to_timestamp()
        # If multiple decisions in same month, keep the last
        pol_m = pol_m[~pol_m.index.duplicated(keep="last")]
        df["policy_rate_pct"] = pol_m.reindex(monthly_idx).ffill()

    # Add lending rates (quarterly, forward-fill)
    taux_map = {
        "Crédits immobiliers": "lending_rate_credits_immobiliers_pct",
        "Global": "lending_rate_global_pct",
        "Crédits à l'équipement": "lending_rate_credits_equipement_pct",
        "Crédits à la consommation": "lending_rate_credits_consommation_pct",
    }
    for src_col, dst_col in taux_map.items():
        if src_col in taux.columns:
            df[dst_col] = taux[src_col].reindex(monthly_idx).ffill()

    # Compute growth rates
    # Monthly log growth for Murabaha
    df["murabaha_immobiliere_growth_yoy_pct"] = (
        df["murabaha_immobiliere_kDH"].pct_change(periods=12) * 100
    )
    df["murabaha_total_growth_yoy_pct"] = (
        df["murabaha_total_kDH"].pct_change(periods=12) * 100
    )
    # Conventional habitat YoY (annual frequency, NaN otherwise)
    df["credit_habitat_growth_yoy_pct"] = (
        df["credit_habitat_MDH"].pct_change(periods=12) * 100
    )

    # Compute penetration ratio: murabaha_immobiliere / (murabaha_immobiliere + credit_habitat)
    # Note: both in different units (kDH vs MDH). Convert.
    df["murabaha_immobiliere_MDH"] = df["murabaha_immobiliere_kDH"] / 1000  # kDH → MDH
    df["penetration_murabaha_in_habitat_pct"] = (
        df["murabaha_immobiliere_MDH"]
        / (df["murabaha_immobiliere_MDH"] + df["credit_habitat_MDH"])
        * 100
    )

    # Save
    df.to_csv(OUT)
    print(f"Saved: {OUT}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df.index.min()} -> {df.index.max()}")
    print(f"\nKey columns non-null counts:")
    for col in df.columns:
        nn = df[col].notna().sum()
        print(f"  {col:50}  {nn}")

    print("\nLast 12 rows:")
    print(df.tail(12).to_string())


if __name__ == "__main__":
    main()