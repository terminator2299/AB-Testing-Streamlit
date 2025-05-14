# ab_core/analysis.py

import pandas as pd
from scipy.stats import chi2_contingency

def analyze(data):
    """
    Performs a Chi-square test for independence between variants and conversions.

    Args:
        data (pd.DataFrame): DataFrame with columns ['user_id', 'variant', 'converted']

    Returns:
        summary_df (pd.DataFrame): Summary statistics per variant
        p_value (float): P-value from chi-square test
    """
    summary = data.groupby("variant")["converted"].agg(['count', 'sum']).reset_index()
    summary.rename(columns={"count": "Total Users", "sum": "Conversions"}, inplace=True)
    summary["Conversion Rate"] = summary["Conversions"] / summary["Total Users"]

    contingency_table = pd.crosstab(data["variant"], data["converted"])
    _, p, _, _ = chi2_contingency(contingency_table)

    return summary, p
