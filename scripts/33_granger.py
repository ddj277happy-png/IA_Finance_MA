"""
Chapter 7 analysis: ADF stationarity, VAR lag selection, Granger causality.

Test:
1. ADF test on Murabaha growth, conventional habitat growth, policy rate
2. VAR(p) lag selection (AIC, BIC, HQIC)
3. Granger causality:
   - Does policy rate Granger-cause Murabaha growth?
   - Does Murabaha growth Granger-cause conventional habitat growth?
   - Does IPAI growth Granger-cause Murabaha growth?

Outputs:
- data/_intermediate/adf_tests.csv
- data/_intermediate/var_lag_selection.csv
- data/_intermediate/granger_tests.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.tsa.api import VAR

DATA = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/real_estate_murabaha.csv")
OUT_TBL = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT_TBL.mkdir(parents=True, exist_ok=True)


def adf_test(series, name, regression="c"):
    """Run ADF test, return results."""
    s = series.dropna()
    result = adfuller(s, regression=regression, autolag="AIC")
    return {
        "series": name,
        "n_obs": len(s),
        "test_stat": result[0],
        "p_value": result[1],
        "lags_used": result[2],
        "n_lags_criterion": result[5] if len(result) > 5 else None,
        "stationary_5pct": result[1] < 0.05,
        "stationary_1pct": result[1] < 0.01,
    }


def main():
    df = pd.read_csv(DATA, index_col=0, parse_dates=True)
    df = df.dropna(subset=["murabaha_immobiliere_kDH", "policy_rate_pct", "ipai_global"])

    # Compute growth rates (stationary)
    df["log_mur"] = np.log(df["murabaha_immobiliere_kDH"])
    df["log_ipai"] = np.log(df["ipai_global"])
    df["log_credit_hab"] = np.log(df["credit_habitat_MDH"])
    df["d_log_mur"] = df["log_mur"].diff()
    df["d_log_ipai"] = df["log_ipai"].diff()
    df["d_log_credit_hab"] = df["log_credit_hab"].diff()
    df["d_policy_rate"] = df["policy_rate_pct"].diff()

    # Also try levels
    df["policy_rate_level"] = df["policy_rate_pct"]

    print("=" * 80)
    print("ADF unit root tests")
    print("=" * 80)

    adf_rows = []
    series_to_test = [
        ("log(Murabaha immobilière)", df["log_mur"]),
        ("Δlog(Murabaha immobilière)", df["d_log_mur"]),
        ("log(IPAI)", df["log_ipai"]),
        ("Δlog(IPAI)", df["d_log_ipai"]),
        ("log(Crédits à l'habitat)", df["log_credit_hab"]),
        ("Δlog(Crédits à l'habitat)", df["d_log_credit_hab"]),
        ("policy_rate (level)", df["policy_rate_level"]),
        ("Δpolicy_rate", df["d_policy_rate"]),
    ]
    for name, s in series_to_test:
        try:
            r = adf_test(s, name)
            adf_rows.append(r)
            print(f"  {name:40} | stat={r['test_stat']:.3f} | p={r['p_value']:.4f} | lags={r['lags_used']} | "
                  f"{'STATIONARY' if r['stationary_5pct'] else 'NON-STATIONARY'}")
        except Exception as e:
            print(f"  {name}: ERROR {e}")

    adf_df = pd.DataFrame(adf_rows)
    adf_df.to_csv(OUT_TBL / "adf_tests.csv", index=False)

    # ==========================
    # VAR lag selection
    # ==========================
    # Use stationary variables: Δlog(Murabaha), Δlog(IPAI), policy_rate_level
    var_data = df[["d_log_mur", "d_log_ipai", "policy_rate_level"]].dropna()
    print(f"\n" + "=" * 80)
    print(f"VAR analysis sample: {len(var_data)} obs ({var_data.index[0].strftime('%Y-%m')} to {var_data.index[-1].strftime('%Y-%m')})")
    print("=" * 80)

    # Cap maxlags at sensible number given small sample
    maxlags = min(8, len(var_data) // 4)
    print(f"Max lags tested: {maxlags}")

    model = VAR(var_data)
    lag_sel = model.select_order(maxlags=maxlags)
    print("\nLag selection criteria:")
    print(lag_sel.summary())

    # Save lag selection results
    lag_rows = []
    for lag in range(1, maxlags + 1):
        try:
            m = model.fit(lag)
            lag_rows.append({
                "lag": lag,
                "AIC": m.aic,
                "BIC": m.bic,
                "HQIC": m.hqic,
            })
        except Exception:
            pass
    pd.DataFrame(lag_rows).to_csv(OUT_TBL / "var_lag_selection.csv", index=False)

    chosen_lag = lag_sel.bic if hasattr(lag_sel, "bic") else 2
    chosen_aic = lag_sel.aic if hasattr(lag_sel, "aic") else 2
    print(f"\nBIC-optimal lag: {chosen_lag}")
    print(f"AIC-optimal lag: {chosen_aic}")

    # ==========================
    # Granger causality tests
    # ==========================
    print("\n" + "=" * 80)
    print(f"Granger causality tests (max lag = {chosen_lag})")
    print("=" * 80)

    pairs = [
        ("policy_rate_level -> Δlog(Murabaha)", "d_log_mur", "policy_rate_level"),
        ("Δlog(Murabaha) -> policy_rate_level", "policy_rate_level", "d_log_mur"),
        ("policy_rate_level -> Δlog(Crédits à l'habitat)", "d_log_credit_hab", "policy_rate_level"),
        ("Δlog(IPAI) -> Δlog(Murabaha)", "d_log_mur", "d_log_ipai"),
        ("Δlog(Murabaha) -> Δlog(Crédits à l'habitat)", "d_log_credit_hab", "d_log_mur"),
        ("Δlog(Crédits à l'habitat) -> Δlog(Murabaha)", "d_log_mur", "d_log_credit_hab"),
    ]

    granger_rows = []
    for label, effect, cause in pairs:
        try:
            test_data = var_data[[effect, cause]].dropna() if cause in var_data.columns else None
            if test_data is None:
                # Use broader df
                if effect == "d_log_credit_hab" or cause == "d_log_credit_hab":
                    test_data = df[[effect, cause]].dropna()
                else:
                    test_data = var_data[[effect, cause]].dropna()
            # Note: grangercausalitytests expects [effect, cause] columns
            gc = grangercausalitytests(test_data, maxlag=chosen_lag, verbose=False)
            # Get minimum p-value across lags
            min_p = min(gc[i+1][0]["ssr_ftest"][1] for i in range(chosen_lag))
            best_lag = min(range(1, chosen_lag+1),
                           key=lambda i: gc[i][0]["ssr_ftest"][1])
            best_f = gc[best_lag][0]["ssr_ftest"][0]
            best_p = gc[best_lag][0]["ssr_ftest"][1]
            granger_rows.append({
                "test": label,
                "best_lag": best_lag,
                "F_stat": best_f,
                "p_value_min_lag": min_p,
                "F_stat_at_best_lag": best_f,
                "p_value": best_p,
                "rejects_5pct": best_p < 0.05,
                "rejects_1pct": best_p < 0.01,
            })
            print(f"  {label}")
            print(f"    best_lag={best_lag}, F={best_f:.3f}, p={best_p:.4f}, "
                  f"min_p_over_lags={min_p:.4f} {'***' if best_p<0.01 else '**' if best_p<0.05 else ''}")
            # Also show all lags
            for i in range(1, chosen_lag + 1):
                f, p, _, _ = gc[i][0]["ssr_ftest"]
                print(f"      lag={i}: F={f:.3f}, p={p:.4f}")
        except Exception as e:
            print(f"  {label}: ERROR {e}")

    granger_df = pd.DataFrame(granger_rows)
    granger_df.to_csv(OUT_TBL / "granger_tests.csv", index=False)
    print(f"\nSaved: {OUT_TBL / 'granger_tests.csv'}")


if __name__ == "__main__":
    main()