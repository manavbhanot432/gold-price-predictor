"""Gold Price Prediction ML Application"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
import os
warnings.filterwarnings('ignore')

class GoldPricePredictorApp:
    def __init__(self):
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        self.models = {}
        self.results = {}
        self.feature_names = []

    def generate_synthetic_data(self, num_days=2500):
        print("=" * 60)
        print("GENERATING SYNTHETIC GOLD PRICE DATA")
        print("=" * 60)
        np.random.seed(42)
        dates = pd.date_range(start='2016-06-01', periods=num_days, freq='D')
        base_price = 1200
        trend = np.linspace(0, 400, num_days)
        seasonal = 100 * np.sin(np.linspace(0, 8*np.pi, num_days))
        noise = np.random.normal(0, 30, num_days)
        prices = base_price + trend + seasonal + noise
        prices = np.maximum(prices, 800)
        df = pd.DataFrame({'Date': dates, 'Close': prices, 'High': prices + np.random.uniform(5, 25, num_days),
                          'Low': prices - np.random.uniform(5, 25, num_days), 
                          'Open': prices + np.random.uniform(-10, 10, num_days),
                          'Volume': np.random.uniform(100000, 500000, num_days)})
        df.set_index('Date', inplace=True)
        self.data = df
        print(f"\n✓ Synthetic data generated")
        print(f"  Shape: {self.data.shape}")
        print(f"  Date range: {self.data.index[0].date()} to {self.data.index[-1].date()}")
        print(f"  Price range: ${self.data['Close'].min():.2f} - ${self.data['Close'].max():.2f}")

    def preprocess_data(self):
        print("\n" + "=" * 60)
        print("DATA PREPROCESSING & FEATURE ENGINEERING")
        print("=" * 60)
        df = self.data[['Close']].copy()
        df.columns = ['Price']
        print(f"\nOriginal data points: {len(df)}")
        df['SMA_5'] = df['Price'].rolling(window=5).mean()
        df['SMA_20'] = df['Price'].rolling(window=20).mean()
        df['SMA_50'] = df['Price'].rolling(window=50).mean()
        df['Momentum'] = df['Price'].diff()
        df['ROC'] = df['Price'].pct_change() * 100
        df.dropna(inplace=True)
        print(f"Data points after feature engineering: {len(df)}")
        self.feature_names = ['Price', 'SMA_5', 'SMA_20', 'SMA_50', 'Momentum', 'ROC']
        X = df[self.feature_names].values
        y = df['Price'].values
        X = self.scaler_X.fit_transform(X)
        y = self.scaler_y.fit_transform(y.reshape(-1, 1)).ravel()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        print(f"\n✓ Data preprocessed successfully")
        print(f"  Features: {', '.join(self.feature_names)}")
        print(f"  Training set size: {len(self.X_train)}")
        print(f"  Test set size: {len(self.X_test)}")

    def train_svm(self):
        print("\n" + "=" * 60)
        print("TRAINING SVM MODEL")
        print("=" * 60)
        svm_model = SVR(kernel='rbf', C=100, epsilon=0.1)
        svm_model.fit(self.X_train, self.y_train)
        y_train_pred = svm_model.predict(self.X_train)
        y_test_pred = svm_model.predict(self.X_test)
        train_rmse = np.sqrt(mean_squared_error(self.y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(self.y_test, y_test_pred))
        test_r2 = r2_score(self.y_test, y_test_pred)
        test_mae = mean_absolute_error(self.y_test, y_test_pred)
        self.models['SVM'] = svm_model
        self.results['SVM'] = {'y_test_pred': y_test_pred, 'test_rmse': test_rmse, 'test_r2': test_r2, 'test_mae': test_mae}
        print(f"✓ SVM model trained - Test RMSE: {test_rmse:.4f}, R²: {test_r2:.4f}, MAE: {test_mae:.4f}")

    def train_random_forest(self):
        print("\n" + "=" * 60)
        print("TRAINING RANDOM FOREST MODEL")
        print("=" * 60)
        rf_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
        rf_model.fit(self.X_train, self.y_train)
        y_test_pred = rf_model.predict(self.X_test)
        test_rmse = np.sqrt(mean_squared_error(self.y_test, y_test_pred))
        test_r2 = r2_score(self.y_test, y_test_pred)
        test_mae = mean_absolute_error(self.y_test, y_test_pred)
        self.models['RandomForest'] = rf_model
        self.results['RandomForest'] = {'y_test_pred': y_test_pred, 'test_rmse': test_rmse, 'test_r2': test_r2, 
                                       'test_mae': test_mae, 'feature_importance': rf_model.feature_importances_}
        print(f"✓ Random Forest trained - Test RMSE: {test_rmse:.4f}, R²: {test_r2:.4f}, MAE: {test_mae:.4f}")

    def train_neural_network(self):
        print("\n" + "=" * 60)
        print("TRAINING NEURAL NETWORK MODEL")
        print("=" * 60)
        nn_model = MLPRegressor(hidden_layer_sizes=(100, 50, 25), max_iter=500, learning_rate_init=0.01, 
                               random_state=42, early_stopping=True, validation_fraction=0.1)
        nn_model.fit(self.X_train, self.y_train)
        y_test_pred = nn_model.predict(self.X_test)
        test_rmse = np.sqrt(mean_squared_error(self.y_test, y_test_pred))
        test_r2 = r2_score(self.y_test, y_test_pred)
        test_mae = mean_absolute_error(self.y_test, y_test_pred)
        self.models['NeuralNetwork'] = nn_model
        self.results['NeuralNetwork'] = {'y_test_pred': y_test_pred, 'test_rmse': test_rmse, 'test_r2': test_r2, 'test_mae': test_mae}
        print(f"✓ Neural Network trained - Test RMSE: {test_rmse:.4f}, R²: {test_r2:.4f}, MAE: {test_mae:.4f}")

    def compare_models(self):
        print("\n" + "=" * 60)
        print("MODEL COMPARISON")
        print("=" * 60)
        data = [{'Model': name, 'Test RMSE': res['test_rmse'], 'Test R²': res['test_r2'], 'Test MAE': res['test_mae']} 
                for name, res in self.results.items()]
        df = pd.DataFrame(data)
        print("\n" + df.to_string(index=False))
        best = df.loc[df['Test R²'].idxmax(), 'Model']
        print(f"\n✓ Best model: {best}")
        return df

    def generate_visualizations(self):
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATIONS")
        print("=" * 60)
        os.makedirs('./results', exist_ok=True)
        y_test_actual = self.scaler_y.inverse_transform(self.y_test.reshape(-1, 1)).ravel()
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        for idx, (name, res) in enumerate(self.results.items()):
            y_pred = self.scaler_y.inverse_transform(res['y_test_pred'].reshape(-1, 1)).ravel()
            axes[idx].plot(y_test_actual, label='Actual', linewidth=2, color='blue')
            axes[idx].plot(y_pred, label='Predicted', linewidth=2, color='red', alpha=0.7)
            axes[idx].set_title(f'{name}', fontweight='bold')
            axes[idx].set_xlabel('Time Steps')
            axes[idx].set_ylabel('Gold Price ($)')
            axes[idx].legend()
            axes[idx].grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('./results/01_predictions_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: 01_predictions_comparison.png")
        plt.close()
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        models_list = list(self.results.keys())
        test_rmse = [self.results[m]['test_rmse'] for m in models_list]
        test_mae = [self.results[m]['test_mae'] for m in models_list]
        test_r2 = [self.results[m]['test_r2'] for m in models_list]
        axes[0].bar(models_list, test_rmse, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[0].set_title('Test RMSE', fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
        axes[1].bar(models_list, test_mae, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[1].set_title('Test MAE', fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        axes[2].bar(models_list, test_r2, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[2].set_title('Test R² Score', fontweight='bold')
        axes[2].grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('./results/02_model_performance.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: 02_model_performance.png")
        plt.close()
        
        if 'RandomForest' in self.results and 'feature_importance' in self.results['RandomForest']:
            importance = self.results['RandomForest']['feature_importance']
            fig, ax = plt.subplots(figsize=(10, 6))
            sorted_idx = np.argsort(importance)[::-1]
            ax.barh(range(len(importance)), importance[sorted_idx], color='#4ECDC4')
            ax.set_yticks(range(len(importance)))
            ax.set_yticklabels([self.feature_names[i] for i in sorted_idx])
            ax.set_xlabel('Feature Importance')
            ax.set_title('Random Forest - Feature Importance', fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.savefig('./results/03_feature_importance.png', dpi=300, bbox_inches='tight')
            print("✓ Saved: 03_feature_importance.png")
            plt.close()
        
        print("✓ All visualizations generated successfully")

    def run(self):
        print("\n" + "█" * 60)
        print("█" + "  GOLD PRICE PREDICTION ML APPLICATION".center(58) + "█")
        print("█" * 60 + "\n")
        self.generate_synthetic_data()
        self.preprocess_data()
        self.train_svm()
        self.train_random_forest()
        self.train_neural_network()
        self.compare_models()
        self.generate_visualizations()
        print("\n" + "=" * 60)
        print("APPLICATION EXECUTION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nResults saved in './results/' directory")

if __name__ == "__main__":
    app = GoldPricePredictorApp()
    app.run()
