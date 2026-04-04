# 🌍 Weather Trend Forecasting — Global Climate Analysis

> **PM Accelerator Technical Assessment | Data Science & Backend Engineering**

PM Accelerator is the #1 product manager community in the world. Our mission is to 
empower aspiring and experienced product managers with the tools, mentorship, and 
real-world experience needed to accelerate their careers in product management.
🌐 [www.pmaccelerator.io](https://www.pmaccelerator.io)



# 📌 Project Overview

This project analyzes the **Global Weather Repository** dataset from Kaggle — 
containing over **133,000 rows** and **41 features** of daily weather data from 
cities worldwide — to forecast future weather trends using advanced data science 
techniques.


# 📁 Project Structure
weather-project/
├── data-science/
│   ├── notebook.ipynb          # Main analysis notebook
│   ├── GlobalWeatherRepository.csv  # Dataset (from Kaggle)
│   └── weather_map.html        # Interactive world map output
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic validators
│   ├── crud.py                 # CRUD operations
│   ├── export.py               # Data export logic
│   └── requirements.txt        # Backend dependencies
├── Weather_Data_Science_Guide.docx  # Full project report
└── README.md

# 🔬 Data Science — What Was Done

# Dataset
Source: [Kaggle — Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)
- Rows: 133,123 | **Features:** 41
- Date Range: May 2024 — April 2026

# Steps Completed

# 1. Data Cleaning & Preprocessing
- Checked and confirmed zero missing values and zero duplicate rows
- Converted `last_updated` column to proper datetime format
- Generated descriptive statistics across all 41 features

# 2. Exploratory Data Analysis (EDA)
- Temperature distribution — histogram, boxplot, top 20 hottest countries
- Correlation heatmap across all numeric features
- Precipitation analysis — wettest countries, temperature vs rainfall scatter

# 3. Anomaly Detection
- Used **Isolation Forest** (scikit-learn) with 5% contamination rate
- Identified extreme weather events across temperature, humidity, wind, and pressure
- Visualized anomalies as red dots vs normal blue dots on scatter plots

# 4. Time Series Forecasting
- Aggregated data to daily global average temperature
- Split: training data vs last 30 days as test set
- Built and compared 3 models:

| Model | MAE | RMSE |
|-------|-----|------|
| ARIMA | 1.26°C | 1.39°C |
| Prophet | 0.74°C | 0.82°C |
| **Ensemble (70% Prophet + 30% ARIMA)** | **0.30°C** | **0.37°C** |
- Ensemble reduced error by **76% compared to ARIMA**

# 5. Feature Importance
- Trained **Random Forest** on all 41 features
- Top features: temperature_fahrenheit, feels_like_fahrenheit, feels_like_celsius
- Confirms temperature-related variables dominate prediction

# 6. Spatial Analysis
- Built interactive world map using **folium**
- Red markers = avg temp above 25°C | Blue = cooler locations
- Clickable popups showing city, country, temperature, humidity

# 7. Air Quality Analysis
- Analyzed Carbon Monoxide, Ozone, NO2, SO2 by country
- Calculated correlation between each pollutant and temperature



# 🚀 How to Run

# Data Science Notebook

# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels prophet plotly folium shap openpyxl jupyter

# Navigate to data-science folder
cd data-science

# Open notebook in VS Code or run:
jupyter notebook notebook.ipynb



# 📦 Requirements
# Data Science
-pandas
-Numpy
-Scikkit-learn
-Seaborn
-Matplotlib
-Prophet
-jupyter
-shap
-openpyxl
-plotly
-statsmodel
-folium



# 📊 Key Insights

1. **Ensemble models win** — combining ARIMA + Prophet reduced forecast error by 76%
2. **Prophet handles seasonality better** — captured yearly temperature cycles precisely
3. **Anomalies cluster in winter** — January cold snaps are the most extreme events
4. **Geography drives temperature** — equatorial regions consistently hotter globally
5. **Air quality correlates with heat** — ozone levels increase with temperature



# 👤 Author
Opara Marvellous Uzoma
Built as part of the PM Accelerator Technical Assessment.

🌐 [www.pmaccelerator.io](https://www.pmaccelerator.io)
