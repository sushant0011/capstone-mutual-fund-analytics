"""
Simple Fund Recommender by Risk Appetite
Input: risk_appetite (Low/Moderate/High)
Output: Top 3 funds by Sharpe ratio within matching risk grade
"""

import pandas as pd

def recommend_funds(risk_appetite, risk_metrics_df, top_n=3):
    """
    Recommend funds based on risk appetite.
    
    Parameters:
    - risk_appetite: 'Low', 'Moderate', or 'High'
    - risk_metrics_df: DataFrame with annual_return, annual_volatility, sharpe_ratio
    - top_n: Number of recommendations
    
    Returns: Top N funds DataFrame
    """
    df = risk_metrics_df.copy()
    
    # Normalize metrics
    df['return_score'] = (df['annual_return'] - df['annual_return'].min()) / (df['annual_return'].max() - df['annual_return'].min() + 1e-8)
    df['volatility_score'] = (df['annual_volatility'] - df['annual_volatility'].min()) / (df['annual_volatility'].max() - df['annual_volatility'].min() + 1e-8)
    df['sharpe_score'] = (df['sharpe_ratio'] - df['sharpe_ratio'].min()) / (df['sharpe_ratio'].max() - df['sharpe_ratio'].min() + 1e-8)
    
    if risk_appetite.lower() == 'low':
        df['rank_score'] = 0.2 * df['volatility_score'] + 0.8 * df['sharpe_score']
    elif risk_appetite.lower() == 'moderate':
        df['rank_score'] = 0.3 * df['volatility_score'] + 0.4 * df['return_score'] + 0.3 * df['sharpe_score']
    elif risk_appetite.lower() == 'high':
        df['rank_score'] = 0.5 * df['return_score'] + 0.5 * df['sharpe_score']
    else:
        raise ValueError("Risk appetite must be 'Low', 'Moderate', or 'High'")
    
    return df.sort_values('rank_score', ascending=False).head(top_n)

if __name__ == "__main__":
    # Example usage
    metrics = pd.read_csv('data/processed/var_cvar_report.csv')
    
    for risk in ['Low', 'Moderate', 'High']:
        print(f"\n{risk} Risk Appetite Recommendations:")
        recs = recommend_funds(risk, metrics)
        print(recs[['scheme_name', 'annual_return', 'annual_volatility', 'sharpe_ratio']])
