"""
Chapter 7 extension: impulse response functions and forecast error variance decomposition.

Plot Cholesky IRF for the VAR(1):
  [Δlog(Murabaha), Δlog(IPAI), policy_rate_level]

Outputs:
- figures/fig5_irf.png — IRF of Murabaha to each shock
- figures/fig6_fevd.png — forecast error variance decomposition
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.api import VAR

plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

DATA = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/real_estate_murabaha.csv")
OUT_FIG = Path(r"D:/ProjectforMM/IA_Finance_MA01/figures")
OUT_TBL = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT_TBL.mkdir(parents=True, exist_ok=True)

ORDER = ["d_log_mur", "d_log_ipai", "policy_rate_level"]
LABELS = {
    "d_log_mur": "Δlog(Murabaha)",
    "d_log_ipai": "Δlog(IPAI)",
    "policy_rate_level": "Policy Rate",
}
COLORS = {"d_log_mur": "#d62728", "d_log_ipai": "#1f77b4", "policy_rate_level": "#2ca02c"}


def main():
    df = pd.read_csv(DATA, index_col=0, parse_dates=True)
    df["log_mur"] = np.log(df["murabaha_immobiliere_kDH"])
    df["log_ipai"] = np.log(df["ipai_global"])
    df["d_log_mur"] = df["log_mur"].diff()
    df["d_log_ipai"] = df["log_ipai"].diff()

    # Build var_data with the correct column names
    var_data = df[["d_log_mur", "d_log_ipai", "policy_rate_pct"]].dropna()
    var_data = var_data.rename(columns={"policy_rate_pct": "policy_rate_level"})
    print(f"VAR sample: {len(var_data)} obs ({var_data.index[0].strftime('%Y-%m')} to {var_data.index[-1].strftime('%Y-%m')})")

    model = VAR(var_data)
    # Use BIC-optimal lag = 1 (parsimonious, avoids overfitting small sample)
    res = model.fit(1)
    print("\n" + "=" * 80)
    print("VAR(1) summary")
    print("=" * 80)
    print(res.summary())

    # ==========================
    # Impulse response (Cholesky: order = MUR, IPAI, POLICY)
    # ==========================
    periods = 24
    irf = res.irf(periods=periods)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for i, target in enumerate(ORDER):
        ax = axes[i]
        for j, source in enumerate(ORDER):
            ir = irf.irfs[:, i, j]
            # Confidence band (95% asymptotic, ~±2*se)
            ax.plot(irf.irfs[:, i, j], color=COLORS[source], linewidth=2, label=LABELS[source])
            se = irf.stderr(orth=False)[:, i, j] if hasattr(irf, "stderr") else None
            # asymptotic SE if available
            ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
        ax.set_xlabel("Periods ahead")
        ax.set_ylabel(f"Response of {LABELS[target]}")
        ax.set_title(f"IRF: → {LABELS[target]}")
        ax.legend(loc="best", fontsize=9)
        ax.grid(True, alpha=0.3)
    fig.suptitle("VAR(1) Orthogonalized Impulse Response (Cholesky ordering: Murabaha → IPAI → Policy rate)", fontsize=12)
    fig.tight_layout()
    plt.savefig(OUT_FIG / "fig5_irf.png", dpi=150)
    plt.close()
    print(f"\nSaved: {OUT_FIG / 'fig5_irf.png'}")

    # ==========================
    # FEVD
    # ==========================
    fevd = res.fevd(periods=12)
    # Inspect shape
    decomp = fevd.decomp
    print(f"\nFEVD decomp shape: {decomp.shape}")
    # Try accessing via .summary() then tabulate manually
    # Manually compute via IRF: sum_{k=0..H} (e_i' Psi_k B B' Psi_k' e_j)^2 / sum_k overall
    # Simpler: use irfs to compute
    horizons = [1, 3, 6, 12]

    # Build FEVD by iterating horizons
    fevd_rows = []
    # decomp shape is (n_vars, n_periods, n_vars) = (3, 12, 3)
    # axis 0 = target variable, axis 1 = horizon, axis 2 = source shock
    for h_idx, h in enumerate(horizons):
        try:
            row = [decomp[ORDER.index("d_log_mur"), h_idx, ORDER.index(s)] for s in ORDER]
            print(f"h={h}: " + ", ".join(f"{LABELS[s]}={v:.3f}" for s, v in zip(ORDER, row)))
            for i, target in enumerate(ORDER):
                for j, source in enumerate(ORDER):
                    fevd_rows.append({
                        "horizon": h,
                        "target": target,
                        "source": source,
                        "share": decomp[i, h_idx, j],
                    })
        except Exception as e:
            print(f"h={h} ERROR: {e}")

    fevd_df = pd.DataFrame(fevd_rows)
    fevd_df.to_csv(OUT_TBL / "fevd_table.csv", index=False)

    # Print FEVD summary
    print("\n" + "=" * 80)
    print("Forecast Error Variance Decomposition (Δlog(Murabaha))")
    print("=" * 80)
    print(f"{'Horizon':<10}" + "".join(f"{LABELS[s]:>25}" for s in ORDER))
    for h_idx, h in enumerate(horizons):
        try:
            row = [decomp[ORDER.index("d_log_mur"), h_idx, ORDER.index(s)] for s in ORDER]
            print(f"h={h:<8}" + "".join(f"{v:>25.3f}" for v in row))
        except Exception as e:
            print(f"h={h}: {e}")

    # Stacked bar plot for ALL three targets (better visualization)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for ax_i, target in enumerate(ORDER):
        ax = axes[ax_i]
        x = np.arange(len(horizons))
        bottoms = np.zeros(len(horizons))
        for j, src in enumerate(ORDER):
            vals = [decomp[ORDER.index(target), h_idx, ORDER.index(src)] for h_idx, _ in enumerate(horizons)]
            ax.bar(x, vals, 0.6, bottom=bottoms, color=COLORS[src], label=LABELS[src])
            bottoms += np.array(vals)
        ax.set_xticks(x)
        ax.set_xticklabels([f"h={h}" for h in horizons])
        ax.set_ylabel("Share of FEV")
        ax.set_title(f"FEVD: {LABELS[target]}")
        ax.set_ylim(0, 1)
        ax.grid(True, axis="y", alpha=0.3)
        if ax_i == 2:
            ax.legend(loc="best", fontsize=9)
    fig.suptitle("VAR(1) Forecast Error Variance Decomposition", fontsize=13)
    fig.tight_layout()
    plt.savefig(OUT_FIG / "fig6_fevd.png", dpi=150)
    plt.close()
    print(f"Saved: {OUT_FIG / 'fig6_fevd.png'}")


if __name__ == "__main__":
    main()