import sys
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import numpy as np

def main():
    try:
        content = sys.stdin.read()
        from io import StringIO
        df = pd.read_csv(StringIO(content))

        if df.empty:
            raise ValueError("Arquivo CSV vazio.")

        if not {'ano', 'semestre', 'desistentes'}.issubset(df.columns):
            raise ValueError("Colunas essenciais ausentes no CSV.")

        # Preparo dos dados
        X = df[['ano', 'semestre']].values
        y = df['desistentes'].values

        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_poly)

        model = LinearRegression()
        model.fit(X_scaled, y)

        # Previsão futura
        future_periods = [(ano, sem) for ano in range(2024, 2027) for sem in [1, 2]]
        future_X = np.array(future_periods)
        future_poly = poly.transform(future_X)
        future_scaled = scaler.transform(future_poly)
        future_preds = model.predict(future_scaled)

        future_preds = [max(0, round(p)) for p in future_preds]  # Não deixar valores negativos

        output = {
            "future_labels": [f"{ano}.{sem}" for ano, sem in future_periods],
            "future_predictions": future_preds
        }

        print(json.dumps(output))

    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
