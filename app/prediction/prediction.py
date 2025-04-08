from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
class Predictor:
    def __init__(self, df):
        self.df = df
        self.models = {
            'linear': LinearRegression(),
            'ridge': Ridge(),
            'lasso': Lasso(),
            'random_forest': RandomForestRegressor()
        }
        self.best_model = None
        self.best_score = float('-inf')
    def prepare_data(self):
        X = self.df[["ano", "semestre"]].values
        y = self.df.iloc[:, 4:].sum(axis=1).values
        return train_test_split(X, y, test_size=0.2, random_state=42)
    def train_models(self):
        X_train, X_test, y_train, y_test = self.prepare_data()
        
        results = {}
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred)
            results[name] = {
                'model': model,
                'score': score,
                'mse': mean_squared_error(y_test, y_pred)
            }
            
            if score > self.best_score:
                self.best_score = score
                self.best_model = model
                
        return results
    def predict(self, future_periods):
        if self.best_model is None:
            self.train_models()
            
        future_X = np.array([[year, sem] 
                            for year in range(2024, 2027) 
                            for sem in [1, 2]])
        return self.best_model.predict(future_X)
    def plot_predictions(self, future_years):
        results = self.train_models()
        
        plt.figure(figsize=(12, 8))
        
        # Dados históricos
        X = self.df[["ano", "semestre"]].values
        y = self.df.iloc[:, 4:].sum(axis=1).values
        plt.scatter(X[:, 0] + X[:, 1]/2, y, color='blue', label='Dados Históricos')
        
        # Previsões
        future_X = np.array([[year, sem] 
                            for year in future_years 
                            for sem in [1, 2]])
        future_years_plot = np.array([year + sem/2 
                                    for year in future_years 
                                    for sem in [1, 2]])
        for name, result in results.items():
            y_pred = result['model'].predict(future_X)
            plt.plot(future_years_plot, y_pred, '--', label=f'{name} (R²: {result["score"]:.2f})')
        
        plt.xlabel("Ano")
        plt.ylabel("Desistências Previstas")
        plt.title("Previsões de Desistência por Diferentes Modelos")
        plt.legend()
        plt.grid(True)
        plt.show()