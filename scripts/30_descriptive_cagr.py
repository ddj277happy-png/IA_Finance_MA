"""
Chapter 4 analysis: Descriptive statistics + CAGR + penetration ratio + dual-axis chart.

Outputs:
- figures/fig1_dual_axis.png
- figures/fig2_penetration.png
- data/_intermediate/descriptive_stats.csv
- data/_intermediate/cagr_table.csv
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.dates as mdates

plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

DATA = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/real_estate_murabaha.csv")
OUT_FIG = Path(r"D:/ProjectforMM/IA_Finance_MA01/figures")
OUT_FIG.mkdir(parents=True, exist_ok=True)
OUT_TBL = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT_TBL.mkdir(parents=True, exist_ok=True)


def cagr(start_val, end_val, periods):
    """Compound annual growth rate."""
    if start_val is None or end_val is None or start_val <= 0 or periods <= 0:
        return None
    return (end_val / start_val) ** (1.0 / periods) - 1


def main():
    df = pd.read_csv(DATA, index_col=0, parse_dates=True)

    # Convert MDH to MMDH for nicer presentation
    df["murabaha_immobiliere_MMDH"] = df["murabaha_immobiliere_kDH"] / 1000  # kDH → MDH → MMDH
    df["murabaha_immobiliere_MMDH"] = df["murabaha_immobiliere_MMDH"] / 1000  # MDH → MMDH
    df["credit_habitat_MMDH"] = df["credit_habitat_MDH"] / 1000

    # =====================
    # 1. Descriptive stats
    # =====================
    desc_cols = [
        "murabaha_immobiliere_kDH",
        "murabaha_total_kDH",
        "credit_habitat_MDH",
        "ipai_global",
        "policy_rate_pct",
        "lending_rate_credits_immobiliers_pct",
    ]
    desc_labels = {
        "murabaha_immobiliere_kDH": "Murabaha immobilière (kDH)",
        "murabaha_total_kDH": "Total Murabaha (kDH)",
        "credit_habitat_MDH": "Conventional Crédits à l'habitat (MDH)",
        "ipai_global": "IPAI Global (index, T1 2006=100)",
        "policy_rate_pct": "BAM policy rate (%)",
        "lending_rate_credits_immobiliers_pct": "Lending rate — Crédits immobiliers (%)",
    }
    stats = pd.DataFrame(index=desc_cols)
    stats.index = [desc_labels[c] for c in stats.index]
    for col in desc_cols:
        s = df[col].dropna()
        stats.loc[desc_labels[col], "N"] = len(s)
        stats.loc[desc_labels[col], "Mean"] = s.mean()
        stats.loc[desc_labels[col], "Std"] = s.std()
        stats.loc[desc_labels[col], "Min"] = s.min()
        stats.loc[desc_labels[col], "P25"] = s.quantile(0.25)
        stats.loc[desc_labels[col], "Median"] = s.median()
        stats.loc[desc_labels[col], "P75"] = s.quantile(0.75)
        stats.loc[desc_labels[col], "Max"] = s.max()
        stats.loc[desc_labels[col], "Start"] = s.iloc[0] if len(s) > 0 else None
        stats.loc[desc_labels[col], "End"] = s.iloc[-1] if len(s) > 0 else None

    print("=" * 80)
    print("Descriptive statistics")
    print("=" * 80)
    print(stats.to_string(float_format=lambda x: f"{x:,.2f}" if pd.notna(x) else "—"))
    stats.to_csv(OUT_TBL / "descriptive_stats.csv")

    # =====================
    # 2. CAGR table
    # =====================
    cagr_rows = []

    # Murabaha immobilière: full sample (2019-07 → 2025-12)
    s = df["murabaha_immobiliere_kDH"].dropna()
    full_periods = (s.index[-1] - s.index[0]).days / 365.25
    cagr_rows.append({
        "series": "Murabaha immobilière (participatory)",
        "unit": "kDH",
        "start_date": s.index[0].strftime("%Y-%m-%d"),
        "end_date": s.index[-1].strftime("%Y-%m-%d"),
        "start_value": s.iloc[0],
        "end_value": s.iloc[-1],
        "years": full_periods,
        "CAGR": cagr(s.iloc[0], s.iloc[-1], full_periods),
    })

    # Murabaha totale
    s = df["murabaha_total_kDH"].dropna()
    full_periods = (s.index[-1] - s.index[0]).days / 365.25
    cagr_rows.append({
        "series": "Total Murabaha (participatory)",
        "unit": "kDH",
        "start_date": s.index[0].strftime("%Y-%m-%d"),
        "end_date": s.index[-1].strftime("%Y-%m-%d"),
        "start_value": s.iloc[0],
        "end_value": s.iloc[-1],
        "years": full_periods,
        "CAGR": cagr(s.iloc[0], s.iloc[-1], full_periods),
    })

    # Conventional habitat (sparse annual snapshots)
    s = df["credit_habitat_MDH"].dropna().drop_duplicates()  # year-end values, no ffill duplicates
    if len(s) >= 2:
        years = (s.index[-1] - s.index[0]).days / 365.25
        cagr_rows.append({
            "series": "Conventional Crédits à l'habitat",
            "unit": "MDH",
            "start_date": s.index[0].strftime("%Y-%m-%d"),
            "end_date": s.index[-1].strftime("%Y-%m-%d"),
            "start_value": s.iloc[0],
            "end_value": s.iloc[-1],
            "years": years,
            "CAGR": cagr(s.iloc[0], s.iloc[-1], years),
        })

    # Total housing credit = Conventional + Murabaha immobilière (last available)
    conv_last = df["credit_habitat_MDH"].dropna().iloc[-1] / 1000  # MDH → MMDH
    mur_last = df["murabaha_immobiliere_kDH"].dropna().iloc[-1] / 1e6  # kDH → MMDH
    total_last = conv_last + mur_last
    print(f"\nLast available (Dec 2025):")
    print(f"  Conventional Crédits à l'habitat: {conv_last:,.1f} MMDH")
    print(f"  Murabaha immobilière:             {mur_last:,.1f} MMDH")
    print(f"  Total housing credit:             {total_last:,.1f} MMDH")
    print(f"  Murabaha share of total:           {mur_last/total_last*100:.2f}%")

    cagr_df = pd.DataFrame(cagr_rows)
    print("\n" + "=" * 80)
    print("CAGR summary")
    print("=" * 80)
    print(cagr_df.to_string(index=False, float_format=lambda x: f"{x:,.4f}" if isinstance(x, float) else str(x)))
    cagr_df.to_csv(OUT_TBL / "cagr_table.csv", index=False)

    # =====================
    # 3. Penetration ratio
    # =====================
    print("\n" + "=" * 80)
    print("Penetration ratio (Murabaha immobilière / Total housing credit)")
    print("=" * 80)
    pen = df[["penetration_murabaha_in_habitat_pct"]].dropna()
    print(f"N: {len(pen)}")
    print(f"Min:  {pen['penetration_murabaha_in_habitat_pct'].min():.2f}%")
    print(f"Max:  {pen['penetration_murabaha_in_habitat_pct'].max():.2f}%")
    print(f"Mean: {pen['penetration_murabaha_in_habitat_pct'].mean():.2f}%")
    print(f"Last: {pen['penetration_murabaha_in_habitat_pct'].iloc[-1]:.2f}% (Dec 2025)")

    # =====================
    # 4. Dual-axis chart: Murabaha immobilière vs Crédits à l'habitat
    # =====================
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color1 = "#1f77b4"
    color2 = "#d62728"

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Murabaha immobilière (MMDH)", color=color1)
    ax1.plot(df.index, df["murabaha_immobiliere_MMDH"],
             color=color1, linewidth=2, label="Murabaha immobilière (participatory)")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, axis="y", alpha=0.3)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Crédits à l'habitat (MMDH, conventional)", color=color2)
    ax2.plot(df.index, df["credit_habitat_MMDH"],
             color=color2, linewidth=2, linestyle="--", label="Crédits à l'habitat (conventional)")
    ax2.tick_params(axis="y", labelcolor=color2)

    plt.title("Morocco Housing Credit: Murabaha immobilière vs Conventional Crédits à l'habitat\n(Jul 2019 – Dec 2025, MMDH)", fontsize=12)
    fig.tight_layout()

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.savefig(OUT_FIG / "fig1_dual_axis.png", dpi=150)
    plt.close()
    print(f"\nSaved: {OUT_FIG / 'fig1_dual_axis.png'}")

    # =====================
    # 5. Penetration chart
    # =====================
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df["penetration_murabaha_in_habitat_pct"],
            color="#2ca02c", linewidth=2, marker="o", markersize=3, label="Murabaha share of total housing credit")
    ax.set_xlabel("Date")
    ax.set_ylabel("Murabaha immobilière share (%)")
    ax.set_title("Murabaha immobilière Share of Total Housing Credit (Morocco)\nJul 2019 – Dec 2025")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    fig.tight_layout()
    plt.savefig(OUT_FIG / "fig2_penetration.png", dpi=150)
    plt.close()
    print(f"Saved: {OUT_FIG / 'fig2_penetration.png'}")

    # =====================
    # 6. Year-end snapshot table for the report
    # =====================
    print("\n" + "=" * 80)
    print("Year-end snapshot table (Dec each year, MMDH)")
    print("=" * 80)
    year_end = df[df.index.month == 12].copy()
    year_end["murabaha_immobiliere_MMDH"] = year_end["murabaha_immobiliere_kDH"] / 1e6
    year_end["murabaha_total_MMDH"] = year_end["murabaha_total_kDH"] / 1e6
    year_end["credit_habitat_MMDH"] = year_end["credit_habitat_MDH"] / 1000
    year_end["credit_habitat_participatif_flash_MMDH"] = year_end["credit_habitat_participatif_flash_MDH"] / 1000
    snap = year_end[["murabaha_immobiliere_MMDH", "murabaha_total_MMDH",
                     "credit_habitat_MMDH", "credit_habitat_participatif_flash_MMDH",
                     "ipai_global", "policy_rate_pct", "lending_rate_credits_immobiliers_pct"]].round(3)
    print(snap.to_string())
    snap.to_csv(OUT_TBL / "year_end_snapshot.csv")


if __name__ == "__main__":
    main()