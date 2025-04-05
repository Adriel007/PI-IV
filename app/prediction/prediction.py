from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

class Predictor:
    def __init__(self, df):
        self.df = df
        self.model = LinearRegression()

    def train_model(self):
        """Treina o modelo de regressão linear e retorna métricas de desempenho."""
        X = self.df["ano"].values.reshape(-1, 1)
        y = self.df["taxa_desistencia"].values
        self.model.fit(X, y)
        # Predições no conjunto de treinamento para calcular as métricas
        y_pred = self.model.predict(X)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        return mse, r2

    def predict(self, future_years):
        """Prevê a taxa de desistência para os próximos anos."""
        X_future = np.array(future_years).reshape(-1, 1)
        return self.model.predict(X_future)

    def plot_predictions(self, future_years):
        """Plota os dados históricos, a linha de regressão e as previsões futuras, exibindo as métricas."""
        mse, r2 = self.train_model()
        X_hist = self.df["ano"].values.reshape(-1, 1)
        y_hist = self.df["taxa_desistencia"].values

        plt.figure(figsize=(10, 6))
        plt.scatter(X_hist, y_hist, color='blue', label='Dados Históricos')

        # Linha de regressão baseada nos dados históricos
        x_line = np.linspace(min(X_hist), max(X_hist), 100).reshape(-1, 1)
        y_line = self.model.predict(x_line)
        plt.plot(x_line, y_line, color='red', label='Linha de Regressão')

        # Previsões futuras
        X_future = np.array(future_years).reshape(-1, 1)
        y_future = self.predict(future_years)
        plt.scatter(X_future, y_future, color='green', marker='x', s=100, label='Previsões Futuras')

        plt.xlabel("Ano")
        plt.ylabel("Taxa de Desistência")
        plt.title(f"Previsão de Desistência (MSE: {mse:.2f}, R²: {r2:.2f})")
        plt.legend()
        plt.show()
