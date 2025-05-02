import sys
import pandas as pd
import json
import numpy as np
from io import StringIO 
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    try:
        # Read and validate data
        content = sys.stdin.read()
        df = pd.read_csv(StringIO(content))
        
        if df.empty:
            raise ValueError("Empty CSV file.")
            
        required_cols = {'ano', 'semestre', 'desistentes'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns. Needed: {required_cols}")
            
        # Feature Engineering
        df['periodo'] = df['ano'] + df['semestre']/10
        df['ano_norm'] = df['ano'] - df['ano'].min()
        
        # Outlier Detection
        q1 = df['desistentes'].quantile(0.25)
        q3 = df['desistentes'].quantile(0.75)
        iqr = q3 - q1
        df = df[~((df['desistentes'] < (q1 - 1.5*iqr)) | (df['desistentes'] > (q3 + 1.5*iqr)))]
        
        # Prepare data
        X = df[['ano_norm', 'semestre']]
        y = df['desistentes']
        
        # Seasonal Analysis
        if len(df) >= 8:  # Minimum for seasonal decomposition
            ts_data = df.set_index('periodo')['desistentes']
            decomposition = seasonal_decompose(ts_data, period=2)  # Assuming yearly seasonality
            df['seasonal'] = decomposition.seasonal.values
            
        # Correlation Analysis
        corr_matrix = df.corr()
        correlation_data = {
            'labels': corr_matrix.index.tolist(),
            'data': corr_matrix.values.tolist()
        }   
        
        # Model Comparison
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(),
            'Lasso Regression': Lasso(),
            'Random Forest': RandomForestRegressor()
        }
        
        poly = PolynomialFeatures(degree=2, include_bias=False)
        scaler = StandardScaler()
        X_poly = poly.fit_transform(X)
        X_scaled = scaler.fit_transform(X_poly)
        
        # Cross-validation setup
        tscv = TimeSeriesSplit(n_splits=5)
        
        results = {}
        for name, model in models.items():
            # Cross-validation
            cv_scores = cross_val_score(model, X_scaled, y, cv=tscv, scoring='neg_mean_squared_error')
            results[name] = {
                'cv_rmse': np.sqrt(-cv_scores.mean()),
                'cv_scores': np.sqrt(-cv_scores).tolist()
            }
            
            # Full training
            model.fit(X_scaled, y)
            preds = model.predict(X_scaled)
            results[name].update({
                'mae': mean_absolute_error(y, preds),
                'mse': mean_squared_error(y, preds),
                'rmse': np.sqrt(mean_squared_error(y, preds))
            })
        
        # Select best model
        best_model_name = min(results, key=lambda x: results[x]['cv_rmse'])
        best_model = models[best_model_name]
        best_model.fit(X_scaled, y)
        
        # Future predictions
        future_periods = [(ano, sem) for ano in range(2024, 2027) for sem in [1, 2]]
        future_X = pd.DataFrame(future_periods, columns=['ano', 'semestre'])
        future_X['ano_norm'] = future_X['ano'] - df['ano'].min()
        future_X = future_X[['ano_norm', 'semestre']]
        
        future_poly = poly.transform(future_X)
        future_scaled = scaler.transform(future_poly)
        future_preds = best_model.predict(future_scaled)
        future_preds = [max(0, round(p)) for p in future_preds]
        
        # Visualization
        plt.figure(figsize=(12,6))
        plt.plot(df['periodo'], df['desistentes'], label='Actual')
        future_periods_str = [f"{ano}.{sem}" for ano, sem in future_periods]
        plt.plot(future_periods_str, future_preds, 'r--', label='Predicted')
        plt.title('Actual vs Predicted Dropouts')
        plt.xlabel('Period')
        plt.ylabel('Dropouts')
        plt.legend()
        plt.savefig('predictions_plot.png')
        plt.close()
        
        output = {
            "best_model": best_model_name,
            "model_metrics": results,
            "future_labels": future_periods_str,
            "future_predictions": future_preds,
            "correlation_data": correlation_data,
            "historical_data": {
                "labels": df['periodo'].tolist(),
                "values": df['desistentes'].tolist()
            }
        }
        
        print(json.dumps(output))
        
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()