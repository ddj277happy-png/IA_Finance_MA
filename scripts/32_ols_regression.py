"""
Chapter 6 analysis: OLS regression of Murabaha immobilière growth on macro controls.

Model:
  Δlog(Murabaha_immobiliere_t) = α + β1·r_t + β2·Δlog(IPAI_t) + β3·Δlog(Credit_habitat_t) + β4·t + ε_t

With Newey-West HAC standard errors to handle serial correlation and heteroskedasticity.

Compare coefficient on policy rate between Murabaha equation and conventional habitat equation.

Outputs:
- data/_intermediate/ols_main.csv (full-sample OLS with HAC SE)
- data/_intermediate/ols_comparison.csv (side-by-side coef tables)
- figures/fig4_ols.png
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path

plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

DATA = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/real_estate_murabaha.csv")
OUT_TBL = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT_FIG = Path(r"D:/ProjectforMM/IA_Finance_MA01/figures")
OUT_FIG.mkdir(parents=True, exist_ok=True)


def fit_ols(y, X, hac_lags=4):
    """Fit OLS with HAC (Newey-West) standard errors."""
    Xc = sm.add_constant(X)
    model = sm.OLS(y, Xc, missing="drop")
    res = model.fit(cov_type="HAC", cov_kwds={"maxlags": hac_lags})
    return res


def coef_table(res, label):
    """Format OLS results into a tidy DataFrame."""
    out = pd.DataFrame({
        "variable": res.params.index,
        "coef": res.params.values,
        "std_err_hac": res.bse.values,
        "t_stat": res.tvalues.values,
        "p_value": res.pvalues.values,
        "ci_lower": res.conf_int().iloc[:, 0].values,
        "ci_upper": res.conf_int().iloc[:, 1].values,
    })
    out["model"] = label
    return out


def main():
    df = pd.read_csv(DATA, index_col=0, parse_dates=True)
    df = df.dropna(subset=["murabaha_immobiliere_kDH", "policy_rate_pct", "ipai_global"])

    # Compute log differences (monthly growth)
    df["log_mur"] = np.log(df["murabaha_immobiliere_kDH"])
    df["log_ipai"] = np.log(df["ipai_global"])
    df["log_credit_hab"] = np.log(df["credit_habitat_MDH"])
    df["log_mur_diff"] = df["log_mur"].diff()
    df["log_ipai_diff"] = df["log_ipai"].diff()
    df["log_credit_hab_diff"] = df["log_credit_hab"].diff()

    # Trend
    df["trend"] = np.arange(len(df))

    # ==========================
    # Main regression: Murabaha immobilière growth
    # ==========================
    reg_df = df[["log_mur_diff", "policy_rate_pct", "log_ipai_diff", "log_credit_hab_diff", "trend"]].dropna()
    print(f"Main regression sample: {len(reg_df)} months ({reg_df.index[0].strftime('%Y-%m')} to {reg_df.index[-1].strftime('%Y-%m')})")

    y = reg_df["log_mur_diff"]
    X_mur = reg_df[["policy_rate_pct", "log_ipai_diff", "log_credit_hab_diff", "trend"]]
    res_mur = fit_ols(y, X_mur, hac_lags=4)
    print("\n" + "=" * 80)
    print("Main OLS: Δlog(Murabaha immobilière) on policy rate, IPAI growth, conventional habitat growth, trend")
    print("=" * 80)
    print(res_mur.summary())
    coef_df_mur = coef_table(res_mur, "Murabaha immobilière")
    coef_df_mur.to_csv(OUT_TBL / "ols_murabaha_main.csv", index=False)

    # ==========================
    # Comparison regression: Conventional Crédits à l'habitat growth
    # ==========================
    # Conventional habitat series is sparse (year-end only). Use annual growth from year-end snapshots
    reg_df2 = df[["log_credit_hab_diff", "policy_rate_pct", "log_ipai_diff", "trend"]].dropna()
    if len(reg_df2) >= 10:
        print(f"\nConventional habitat regression sample: {len(reg_df2)} obs")
        y2 = reg_df2["log_credit_hab_diff"]
        X2 = reg_df2[["policy_rate_pct", "log_ipai_diff", "trend"]]
        res_conv = fit_ols(y2, X2, hac_lags=2)
        print(res_conv.summary())
        coef_df_conv = coef_table(res_conv, "Crédits à l'habitat (conventional)")
        coef_df_conv.to_csv(OUT_TBL / "ols_conventional.csv", index=False)
    else:
        print(f"\nConventional regression: insufficient obs ({len(reg_df2)}); skipping")
        coef_df_conv = pd.DataFrame()

    # ==========================
    # Comparison table
    # ==========================
    print("\n" + "=" * 80)
    print("Side-by-side coefficient comparison (policy rate elasticity)")
    print("=" * 80)
    if len(coef_df_conv) > 0:
        comp = pd.DataFrame({
            "Murabaha immobilière": coef_df_mur.set_index("variable")["coef"],
            "Murabaha SE (HAC)": coef_df_mur.set_index("variable")["std_err_hac"],
            "Murabaha p": coef_df_mur.set_index("variable")["p_value"],
            "Conventional": coef_df_conv.set_index("variable")["coef"],
            "Conventional SE (HAC)": coef_df_conv.set_index("variable")["std_err_hac"],
            "Conventional p": coef_df_conv.set_index("variable")["p_value"],
        })
        print(comp.to_string(float_format=lambda x: f"{x:,.4f}" if pd.notna(x) else "—"))
        comp.to_csv(OUT_TBL / "ols_comparison.csv")

    # Wald test: difference in policy rate coefficient between models
    # Simple: compute z = (β1 - β2) / sqrt(SE1² + SE2²)
    if len(coef_df_conv) > 0:
        b1 = coef_df_mur.set_index("variable").loc["policy_rate_pct", "coef"]
        se1 = coef_df_mur.set_index("variable").loc["policy_rate_pct", "std_err_hac"]
        b2 = coef_df_conv.set_index("variable").loc["policy_rate_pct", "coef"]
        se2 = coef_df_conv.set_index("variable").loc["policy_rate_pct", "std_err_hac"]
        z_diff = (b1 - b2) / np.sqrt(se1**2 + se2**2)
        from scipy.stats import norm
        p_diff = 2 * (1 - norm.cdf(abs(z_diff)))
        print(f"\nWald test: diff in policy rate coefficient")
        print(f"  β_mur = {b1:.4f}, β_conv = {b2:.4f}, z = {z_diff:.3f}, p = {p_diff:.4f}")

    # ==========================
    # Robustness check: sub-sample regressions
    # ==========================
    print("\n" + "=" * 80)
    print("Robustness: sub-sample regressions (Murabaha)")
    print("=" * 80)
    sub_samples = [
        ("Jul 2019 – Dec 2021", "2019-07-01", "2021-12-31"),
        ("Jan 2022 – Dec 2024", "2022-01-01", "2024-12-31"),
        ("Jan 2025 – Dec 2025", "2025-01-01", "2025-12-31"),
    ]
    rob_rows = []
    for label, start, end in sub_samples:
        sub = reg_df.loc[start:end]
        if len(sub) < 10:
            continue
        y_s = sub["log_mur_diff"]
        X_s = sub[["policy_rate_pct", "log_ipai_diff", "log_credit_hab_diff", "trend"]]
        try:
            r = fit_ols(y_s, X_s, hac_lags=min(4, len(sub)//4))
            ct = coef_table(r, f"sub_{label}")
            ct["sub_sample"] = label
            rob_rows.append(ct)
            print(f"\n  {label} (n={len(sub)}):")
            print(r.summary().tables[1])
        except Exception as e:
            print(f"  {label}: skipped ({e})")

    if rob_rows:
        pd.concat(rob_rows, ignore_index=True).to_csv(OUT_TBL / "ols_robustness_subsamples.csv", index=False)

    # ==========================
    # Plot: actual vs fitted
    # ==========================
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax = axes[0]
    ax.plot(reg_df.index, reg_df["log_mur_diff"], color="#1f77b4", linewidth=1, alpha=0.5, label="Actual Δlog(Murabaha imm.)")
    ax.plot(reg_df.index, res_mur.fittedvalues, color="#d62728", linewidth=2, label="Fitted")
    ax.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax.set_ylabel("Δlog(Murabaha immobilière)")
    ax.set_title("OLS Fit: Actual vs Fitted")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(res_mur.resid.index, res_mur.resid, color="gray", linewidth=1)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Residual")
    ax.set_title("OLS Residuals")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    plt.savefig(OUT_FIG / "fig4_ols.png", dpi=150)
    plt.close()
    print(f"\nSaved: {OUT_FIG / 'fig4_ols.png'}")


if __name__ == "__main__":
    main()