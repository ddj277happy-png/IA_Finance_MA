"""
Chapter 5/6 analysis: Structural break tests (Chow + Bai-Perron) on Murabaha immobilière.

Murabaha immobilière starts Jul-2019. We test for breaks in its level and growth rate.

Outputs:
- data/_intermediate/structural_breaks.csv
- figures/fig3_breaks.png
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import statsmodels.api as sm
from statsmodels.stats.diagnostic import breaks_cusumolsresid

plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

DATA = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/real_estate_murabaha.csv")
OUT_TBL = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT_FIG = Path(r"D:/ProjectforMM/IA_Finance_MA01/figures")
OUT_FIG.mkdir(parents=True, exist_ok=True)


def chow_test(y, X, break_idx):
    """Manual Chow test for a structural break at the given index."""
    n = len(y)
    k = X.shape[1]
    if break_idx < k + 2 or break_idx > n - k - 2:
        return None
    y1, X1 = y.iloc[:break_idx], X.iloc[:break_idx]
    y2, X2 = y.iloc[break_idx:], X.iloc[break_idx:]
    # Full model
    ols_full = sm.OLS(y, sm.add_constant(X)).fit()
    rss_full = ols_full.ssr
    ols1 = sm.OLS(y1, sm.add_constant(X1)).fit()
    ols2 = sm.OLS(y2, sm.add_constant(X2)).fit()
    rss1, rss2 = ols1.ssr, ols2.ssr
    rss_split = rss1 + rss2
    # F statistic
    F_stat = ((rss_full - rss_split) / k) / (rss_split / (n - 2 * k))
    from scipy.stats import f as f_dist
    p_value = 1 - f_dist.cdf(F_stat, k, n - 2 * k)
    return {
        "break_date": y.index[break_idx],
        "break_idx": break_idx,
        "F_stat": F_stat,
        "p_value": p_value,
        "rss_full": rss_full,
        "rss_split": rss_split,
        "coef_pre": ols1.params,
        "coef_post": ols2.params,
    }


def bai_perron_test(y, X, max_breaks=3, min_obs_fraction=0.15):
    """Bai-Perron multiple structural break test (simplified sequential).

    Uses BIC for selecting number of breaks; tests up to max_breaks.
    Returns list of detected break dates."""
    n = len(y)
    min_obs = max(int(n * min_obs_fraction), 5)
    breakpoints = []
    current_y, current_X = y, X
    for _ in range(max_breaks):
        best_bic = np.inf
        best_idx = None
        best_break = None
        # Try every possible break index
        for i in range(min_obs, len(current_y) - min_obs):
            try:
                r = chow_test(current_y, current_X, i)
                if r is None:
                    continue
                # BIC of the split model (vs full)
                bic = len(current_y) * np.log(r["rss_split"] / len(current_y)) + (X.shape[1] * 2) * np.log(len(current_y))
                if bic < best_bic:
                    best_bic = bic
                    best_idx = i
                    best_break = r
            except Exception:
                continue
        if best_break is None:
            break
        # Test if this break is significant at p<0.05
        if best_break["p_value"] > 0.05:
            break
        breakpoints.append(best_break)
        # Split and recurse
        b = best_idx
        current_y_left = current_y.iloc[:b]
        current_X_left = current_X.iloc[:b]
        current_y_right = current_y.iloc[b:]
        current_X_right = current_X.iloc[b:]
        # Process left segment
        for _ in range(max_breaks):
            best_bic2 = np.inf
            best_idx2 = None
            best_break2 = None
            for i in range(min_obs, len(current_y_left) - min_obs):
                try:
                    r2 = chow_test(current_y_left, current_X_left, i)
                    if r2 is None or r2["p_value"] > 0.05:
                        continue
                    bic2 = len(current_y_left) * np.log(r2["rss_split"] / len(current_y_left)) + (X.shape[1] * 2) * np.log(len(current_y_left))
                    if bic2 < best_bic2:
                        best_bic2 = bic2
                        best_idx2 = i
                        best_break2 = r2
                except Exception:
                    continue
            if best_break2 is None:
                break
            breakpoints.append(best_break2)
            current_y_left = current_y_left.iloc[:best_idx2]
            current_X_left = current_X_left.iloc[:best_idx2]
        # Process right segment
        for _ in range(max_breaks):
            best_bic3 = np.inf
            best_idx3 = None
            best_break3 = None
            for i in range(min_obs, len(current_y_right) - min_obs):
                try:
                    r3 = chow_test(current_y_right, current_X_right, i)
                    if r3 is None or r3["p_value"] > 0.05:
                        continue
                    bic3 = len(current_y_right) * np.log(r3["rss_split"] / len(current_y_right)) + (X.shape[1] * 2) * np.log(len(current_y_right))
                    if bic3 < best_bic3:
                        best_bic3 = bic3
                        best_idx3 = i
                        best_break3 = r3
                except Exception:
                    continue
            if best_break3 is None:
                break
            breakpoints.append(best_break3)
            current_y_right = current_y_right.iloc[best_idx3:]
            current_X_right = current_X_right.iloc[best_idx3:]
        break  # only do one top-level pass
    return breakpoints


def main():
    df = pd.read_csv(DATA, index_col=0, parse_dates=True)
    # Use Murabaha immobilière level (kDH) — but it's exponential, use log
    s = df["murabaha_immobiliere_kDH"].dropna()
    # Build regressors: trend + quarter dummies (for seasonality)
    n = len(s)
    y = np.log(s)
    # Trend
    trend = pd.Series(np.arange(1, n + 1), index=s.index, name="trend")
    # Quarter dummies
    X = pd.DataFrame({"trend": trend.values}, index=s.index)
    for q in range(1, 4):
        X[f"q{q}"] = (s.index.quarter == q).astype(int)

    # ==========================
    # 1. Chow test at known dates
    # ==========================
    known_dates = {
        "Mar 2020 (COVID onset)": "2020-03-01",
        "Dec 2020 (COVID easing)": "2020-12-01",
        "Mar 2022 (rate hike start)": "2022-03-01",
        "Sep 2022 (rate hike continue)": "2022-09-01",
        "Mar 2024 (rate cut start)": "2024-03-01",
        "Jun 2024 (rate cut continue)": "2024-06-01",
    }
    print("=" * 80)
    print("Chow tests at pre-specified break dates (log Murabaha immobilière)")
    print("=" * 80)
    chow_results = []
    for label, date_str in known_dates.items():
        target_date = pd.Timestamp(date_str)
        # Find closest index
        idx = s.index.get_indexer([target_date], method="nearest")[0]
        # Ensure enough obs on each side
        if idx < 6 or idx > n - 6:
            continue
        r = chow_test(y, X, idx)
        if r:
            chow_results.append({
                "label": label,
                "break_date": r["break_date"].strftime("%Y-%m-%d"),
                "F_stat": r["F_stat"],
                "p_value": r["p_value"],
                "significant_5pct": r["p_value"] < 0.05,
                "significant_1pct": r["p_value"] < 0.01,
            })
            print(f"  {label:30} | date={r['break_date'].strftime('%Y-%m-%d')} | F={r['F_stat']:.2f} | p={r['p_value']:.4f} {'***' if r['p_value']<0.01 else '**' if r['p_value']<0.05 else ''}")

    chow_df = pd.DataFrame(chow_results)
    chow_df.to_csv(OUT_TBL / "chow_tests_known_dates.csv", index=False)

    # ==========================
    # 2. Bai-Perron (sequential search for unknown break dates)
    # ==========================
    print("\n" + "=" * 80)
    print("Bai-Perron sequential structural break detection")
    print("=" * 80)
    breaks = bai_perron_test(y, X, max_breaks=3)
    bp_results = []
    for b in breaks:
        bp_results.append({
            "break_date": b["break_date"].strftime("%Y-%m-%d"),
            "F_stat": b["F_stat"],
            "p_value": b["p_value"],
            "coef_pre_intercept": b["coef_pre"].iloc[0],
            "coef_pre_trend": b["coef_pre"].iloc[1],
            "coef_post_intercept": b["coef_post"].iloc[0],
            "coef_post_trend": b["coef_post"].iloc[1],
        })
        print(f"  Break at {b['break_date'].strftime('%Y-%m-%d')} | F={b['F_stat']:.2f} | p={b['p_value']:.4f}")
        print(f"    Pre:  intercept={b['coef_pre'].iloc[0]:.4f}, trend={b['coef_pre'].iloc[1]:.4f}")
        print(f"    Post: intercept={b['coef_post'].iloc[0]:.4f}, trend={b['coef_post'].iloc[1]:.4f}")

    bp_df = pd.DataFrame(bp_results)
    bp_df.to_csv(OUT_TBL / "bai_perron_breaks.csv", index=False)

    # ==========================
    # 3. Plot with break dates
    # ==========================
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(s.index, s.values / 1e6, color="#1f77b4", linewidth=2,
            label="Murabaha immobilière (MMDH)")
    ax.set_yscale("log")
    ax.set_xlabel("Date")
    ax.set_ylabel("Murabaha immobilière (MMDH, log scale)")
    ax.set_title("Murabaha immobilière Outstanding with Structural Breaks (Morocco)\nJul 2019 – Dec 2025")
    ax.grid(True, which="both", alpha=0.3)

    # Mark all break dates from Bai-Perron
    colors = ["#d62728", "#2ca02c", "#ff7f0e"]
    for i, b in enumerate(breaks):
        color = colors[i % len(colors)]
        ax.axvline(b["break_date"], color=color, linestyle="--", linewidth=2, alpha=0.7,
                   label=f"BP break {i+1}: {b['break_date'].strftime('%Y-%m')}")
    # Also mark known Chow-tested dates
    for r in chow_results:
        if r["significant_5pct"]:
            ax.axvline(pd.Timestamp(r["break_date"]), color="gray", linestyle=":", linewidth=1, alpha=0.4)

    ax.legend(loc="upper left")
    fig.tight_layout()
    plt.savefig(OUT_FIG / "fig3_breaks.png", dpi=150)
    plt.close()
    print(f"\nSaved: {OUT_FIG / 'fig3_breaks.png'}")

    # Save combined results
    pd.concat([
        chow_df.assign(kind="Chow (known date)"),
        bp_df.assign(kind="Bai-Perron (sequential)"),
    ], ignore_index=True).to_csv(OUT_TBL / "structural_breaks.csv", index=False)


if __name__ == "__main__":
    main()