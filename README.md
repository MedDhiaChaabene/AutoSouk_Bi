# 🚗 AutoSouk BI – Tunisian Used-Car Market Intelligence

**Turning Tunisian automotive market data into actionable insights through Web Scraping, Data Analytics, Business Intelligence, and Machine Learning.**

---

## 📌 Overview

AutoSouk BI is an end-to-end data analytics and machine learning project designed to analyze the Tunisian used-car market.

The project collects vehicle listings from multiple Tunisian automotive platforms, processes and integrates the extracted data into a unified dataset, and transforms it into meaningful market insights through interactive Power BI dashboards and predictive machine learning models.

The main objective is to provide a better understanding of the local automotive market, identify pricing trends, analyze vehicle characteristics, and estimate fair market prices for used cars.

## 🎯 Project Objectives

- **Market Data Collection:** Extract vehicle listings from multiple Tunisian automotive websites.
- **Data Engineering:** Clean, preprocess, standardize, and integrate heterogeneous datasets.
- **Exploratory Data Analysis:** Identify market trends, pricing patterns, and vehicle characteristics.
- **Business Intelligence:** Develop interactive dashboards to visualize key automotive market indicators.
- **Price Prediction:** Build and evaluate machine learning models to estimate used-car prices.
- **Market Intelligence:** Identify potential pricing opportunities and support data-driven purchasing decisions.

## 🛠️ Technologies & Tools

| Category | Technologies |
|---|---|
| Programming | Python |
| Web Scraping | BeautifulSoup, Selenium |
| Data Manipulation | Pandas, NumPy |
| Database | PostgreSQL 16 |
| Machine Learning | LightGBM, Scikit-learn |
| Data Visualization | Power BI |
| Development | Jupyter Notebook, Git |

## 🔄 Project Architecture

The project follows an end-to-end data pipeline:

```text
        DATA SOURCES
              |
              ▼
      WEB SCRAPING
    BeautifulSoup / Selenium
              |
              ▼
       DATA STORAGE
          PostgreSQL
              |
              ▼
      DATA PREPROCESSING
   Cleaning / Transformation
   Standardization / Integration
              |
              ▼
       UNIFIED DATASET
        used_cars_tn.csv
              |
        ┌─────┴─────┐
        ▼           ▼
   POWER BI      MACHINE LEARNING
   DASHBOARDS       LightGBM
        |              |
        ▼              ▼
   MARKET INSIGHTS  PRICE PREDICTION
```

## 🌐 Data Collection

Vehicle listings are collected from several Tunisian automotive platforms using automated web scraping techniques.

**Data sources:**

- Automax
- Automobile.tn
- Automoto
- Baniola
- ScoutCar
- Zmorda

**Scraping technologies:**

- BeautifulSoup for HTML parsing and structured data extraction.
- Selenium for navigating JavaScript-rendered pages and dynamically loaded content.

The extracted listings are integrated into a unified dataset to facilitate further analysis.

## 🧹 Data Preparation & Engineering

Raw data collected from different platforms often contains inconsistencies, missing values, and heterogeneous formats.

The preprocessing pipeline includes:

- Data cleaning and removal of invalid records.
- Handling missing and inconsistent values.
- Standardization of vehicle attributes.
- Data type conversion and formatting.
- Feature preparation and engineering.
- Integration of listings from multiple sources.
- Outlier analysis and treatment.

The resulting dataset is consolidated into `used_cars_tn.csv`.

## 📊 Business Intelligence – Power BI

An interactive Power BI report was developed to explore the Tunisian used-car market through multiple analytical perspectives.

The report includes four analytical pages.

### 1. Market Overview

Provides a high-level understanding of the automotive market through key performance indicators and visualizations.

**Key Performance Indicators:**
- Total number of vehicle listings.
- Price range and median price.
- Mileage range and median mileage.
- Vehicle manufacturing year range.

**Visualizations:**
- Top 10 vehicle brands by listing volume.
- Market share distribution by brand.
- Monthly listing trends and median price evolution.
- Most expensive vehicle brands.
- Least expensive vehicle brands.

### 2. Vehicle Specifications

Explores the technical characteristics and distribution of listed vehicles.

**Key Performance Indicators:**
- Total vehicle listings.
- Price range and median price.
- Mileage range and median mileage.

**Visualizations:**
- Fuel type distribution.
- Fuel preferences by vehicle body type.
- Transmission type distribution and average price.
- Top 10 vehicle body types.
- Price and vehicle characteristics analysis through scatter plots.

### 3. Additional Analytical Pages

The remaining two report pages extend the market analysis with additional analytical perspectives.

## 🤖 Machine Learning – Used-Car Price Prediction

A machine learning pipeline was developed to estimate used-car prices based on vehicle characteristics.

**Algorithm:** LightGBM Regressor

The model uses relevant vehicle attributes to identify pricing patterns and predict estimated market values.

### Model Development

The modeling process includes:

1. Feature selection and preparation.
2. Handling missing values.
3. Feature engineering.
4. Outlier analysis.
5. Model training.
6. Hyperparameter tuning.
7. Model evaluation on unseen test data.

### Model Performance

The tuned LightGBM model achieved the following results on the test dataset:

| Evaluation Metric | Result |
|---|---:|
| MAE | 10,426 TND |
| RMSE | 21,720 TND |
| MAPE | 19.07% |
| R² Score | 0.789 |

These results indicate that the model captures a substantial proportion of the price variation in the test dataset.

*Note: Prediction errors can vary depending on vehicle characteristics and price segments. High-priced vehicles present additional prediction challenges.*


## 📈 Expected Outcomes

AutoSouk BI demonstrates how data engineering, analytics, and machine learning can be combined to address a real-world business problem.

The project delivers:

- A consolidated dataset of Tunisian automotive listings.
- Insights into vehicle brands, pricing, and market distribution.
- Interactive business intelligence dashboards.
- A machine learning model for used-car price estimation.
- A data-driven approach to understanding the Tunisian second-hand automotive market.


## 👨‍💻 Author

**Mohamed Dhia Chaabene**

Business Intelligence Student | Data Analytics & Machine Learning

**Technical Interests:**
- Business Intelligence & Data Visualization
- Data Engineering & ETL
- Machine Learning
- Predictive Analytics
