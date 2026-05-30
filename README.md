# Gold Price Prediction Machine Learning Application

## Overview
A comprehensive machine learning application that predicts future gold prices using three supervised learning algorithms: Support Vector Machines (SVM), Random Forests, and Neural Networks.

## Project Structure
```
gold-price-predictor/
├── gold_price_predictor.py                      # Main application file
├── Gold_Price_Prediction_Report.docx            # Comprehensive project report (APA format)
├── README.md                                     # This file
└── results/
    ├── 01_predictions_comparison.png            # Model predictions vs actual prices
    ├── 02_model_performance.png                 # Performance metrics comparison
    └── 03_feature_importance.png                # Random Forest feature importance
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Required Libraries
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Usage

### Running the Application
```bash
python gold_price_predictor.py
```

The application will:
1. Generate synthetic gold price data (2,500 historical observations)
2. Preprocess data and engineer technical indicators
3. Train three ML models on the dataset
4. Evaluate performance on test set
5. Generate visualization plots and comparison charts
6. Display model performance metrics

### Output
Results are saved in the `results/` directory containing:
- **01_predictions_comparison.png**: Line plots showing model predictions vs actual prices for each algorithm
- **02_model_performance.png**: Bar charts comparing RMSE, MAE, and R² scores across models
- **03_feature_importance.png**: Feature importance ranking from Random Forest model

## Dataset

### Data Description
- **Type**: Synthetic historical gold price data
- **Time Period**: June 2016 - April 2023 (2,500 trading days)
- **Records**: 2,451 after feature engineering
- **Train/Test Split**: 80/20 (1,960 training, 491 test samples)

### Features Engineered
1. **Price**: Daily closing gold price (USD)
2. **SMA_5**: 5-day Simple Moving Average
3. **SMA_20**: 20-day Simple Moving Average
4. **SMA_50**: 50-day Simple Moving Average
5. **Momentum**: Day-over-day price change
6. **ROC**: Rate of Change (percentage)

## Models

### 1. Support Vector Machine (SVM)
- **Algorithm**: Support Vector Regression with RBF kernel
- **Hyperparameters**: C=100, epsilon=0.1
- **Test Performance**: R² = 0.7817, RMSE = 0.0469, MAE = 0.0342

### 2. Random Forest
- **Algorithm**: Ensemble of decision trees with averaging
- **Hyperparameters**: 100 trees, max_depth=20
- **Test Performance**: R² = 0.9961, RMSE = 0.0063, MAE = 0.0016

### 3. Neural Network
- **Architecture**: 6 → 100 → 50 → 25 → 1 neurons
- **Hyperparameters**: learning_rate=0.01, max_iter=500, early_stopping=True
- **Test Performance**: R² = 0.9987, RMSE = 0.0036, MAE = 0.0025

## Results Summary

| Model | Test R² | Test RMSE | Test MAE | Rank |
|-------|---------|-----------|----------|------|
| SVM | 0.7817 | 0.0469 | 0.0342 | 3rd |
| Random Forest | 0.9961 | 0.0063 | 0.0016 | 2nd |
| **Neural Network** | **0.9987** | **0.0036** | **0.0025** | **1st** |

### Key Findings
- **Best Model**: Neural Network with R² = 0.9987
- **Most Important Features**: Current Price and 50-day Moving Average (SMA_50)
- **Performance**: All models significantly outperform baseline, with deep learning achieving exceptional accuracy

## Technical Implementation

### Libraries Used
- **Pandas**: Data manipulation and preprocessing
- **NumPy**: Numerical computations
- **Scikit-learn**: ML algorithms, metrics, preprocessing
- **Matplotlib**: Visualization and plotting

### Preprocessing Pipeline
1. Data normalization using MinMax scaling (0-1 range)
2. Feature engineering with technical indicators
3. Train-test split using chronological order (80-20)
4. Inverse transformation for result visualization

## Key Insights

### Model Performance Analysis
- Neural Network captured 99.87% of price variance, indicating exceptional learning
- Random Forest's strong performance (R² = 0.9961) demonstrates ensemble methods' effectiveness
- SVM underperformed, suggesting kernel limitations or suboptimal hyperparameter tuning

### Feature Importance
- **SMA_50** and **Price** features drive ~60% of Random Forest decisions
- Aligns with technical analysis: long-term trends provide strong prediction signals
- **Momentum** and **ROC** capture short-term volatility patterns

### Practical Applications
- Portfolio hedging and risk management
- Trading strategy development
- Investment decision support
- Market trend analysis

## Limitations & Considerations

1. **Synthetic Data**: Models trained on simulated data; real-world performance may differ
2. **Technical Indicators Only**: Macroeconomic factors (inflation, USD strength, interest rates) excluded
3. **Temporal Stability**: Assumes stable relationships over time; regime changes could invalidate predictions
4. **Overfitting Risk**: High R² scores suggest potential overfitting; validation on unseen data necessary

## Future Improvements

- Implement LSTM networks for better temporal pattern recognition
- Incorporate macroeconomic features (VIX, USD index, inflation)
- Develop ensemble voting combining all three models
- Use cross-validation and backtesting across multiple time periods
- Add real-time prediction capability with model retraining pipelines

## Report & Documentation

A comprehensive report in APA format is included: **Gold_Price_Prediction_Report.docx**

The report contains:
1. Name and Purpose of the Application
2. Algorithms Used (detailed explanations)
3. Dataset Information
4. Libraries, Toolkits, and Framework
5. Application Design and Implementation
6. Instructions for Running the Application
7. Results and Performance Metrics
8. Discussion and Insights
9. References (APA style)

## Contact & License

**Author**: Manav Bhanot  
**Email**: Manavbhanot18@gmail.com  
**Date**: May 29, 2026

This project is part of a Machine Learning course assignment.

---

**Note**: This application uses synthetic data for demonstration purposes. For real-world deployment, integrate with actual market data sources and implement continuous model validation and retraining mechanisms.
