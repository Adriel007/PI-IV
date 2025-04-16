from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
import numpy as np
import matplotlib.pyplot as plt

class Predictor:
    def __init__(self, df):
        self.df = df
        self.models = {
            'Linear': LinearRegression(),
            'Ridge': Ridge(),
            'Lasso': Lasso(),
            'RandomForest': RandomForestRegressor(),
            'GradientBoosting': GradientBoostingRegressor(),
            'KNN': KNeighborsRegressor()
        }
        self.best_model = None
        self.best_score = float('-inf')

    def prepare_data(self):
        # Feature engineering: soma colunas a partir da 5ª
        X_raw = self.df[["ano", "semestre"]].values
        y = self.df.iloc[:, 4:].sum(axis=1).values

        # Feature interaction: combinações polinomiais + normalização
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X_raw)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_poly)

        return X_scaled, y

    def train_models(self, cv=5):
        X, y = self.prepare_data()
        results = {}

        for name, model in self.models.items():
            # Cross-validation
            scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
            model.fit(X, y)
            y_pred = model.predict(X)

            results[name] = {
                'model': model,
                'r2': r2_score(y, y_pred),
                'mae': mean_absolute_error(y, y_pred),
                'mse': mean_squared_error(y, y_pred),
                'cv_r2_mean': np.mean(scores),
                'cv_r2_std': np.std(scores)
            }

            if results[name]['cv_r2_mean'] > self.best_score:
                self.best_score = results[name]['cv_r2_mean']
                self.best_model = model

        return results

    def predict(self, future_periods):
        if self.best_model is None:
            self.train_models()

        future_X_raw = np.array([[year, sem]
                                 for year in range(2024, 2027)
                                 for sem in [1, 2]])

        poly = PolynomialFeatures(degree=2, include_bias=False)
        future_poly = poly.fit_transform(future_X_raw)
        scaler = StandardScaler()
        future_scaled = scaler.fit_transform(future_poly)

        return self.best_model.predict(future_scaled)

    def plot_predictions(self, future_years):
        results = self.train_models()

        plt.figure(figsize=(12, 8))

        # Dados históricos
        X_raw = self.df[["ano", "semestre"]].values
        y = self.df.iloc[:, 4:].sum(axis=1).values
        X_plot = X_raw[:, 0] + X_raw[:, 1] / 2
        plt.scatter(X_plot, y, color='black', label='Dados Históricos', alpha=0.6)

        # Futuro
        future_X_raw = np.array([[year, sem]
                                 for year in future_years
                                 for sem in [1, 2]])
        future_plot_x = np.array([year + sem / 2
                                 for year in future_years
                                 for sem in [1, 2]])

        # Feature transform
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly_all = poly.fit_transform(np.vstack((X_raw, future_X_raw)))
        scaler = StandardScaler()
        X_scaled_all = scaler.fit_transform(X_poly_all)

        X_scaled = X_scaled_all[:len(X_raw)]
        future_scaled = X_scaled_all[len(X_raw):]

        for name, result in results.items():
            model = result['model']
            future_y = model.predict(future_scaled)

            plt.plot(future_plot_x, future_y, '--', label=f"{name} (CV R²: {result['cv_r2_mean']:.2f})")

        plt.xlabel("Ano")
        plt.ylabel("Desistências Previstas")
        plt.title("Comparação de Previsões por Modelo de Regressão")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
