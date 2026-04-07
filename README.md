Healthcare Utilization Prediction Using Machine Learning

Predicting Year-2 Office-Based Visits from MEPS Data

Project Overview

This project develops a machine learning framework to predict Year-2 outpatient healthcare utilization using demographic, socioeconomic, health status, and prior utilization data from the Medical Expenditure Panel Survey (MEPS). The goal is to support data-driven healthcare planning by identifying patterns in patient utilization and estimating future demand for outpatient services.

The analysis applies multiple predictive modeling techniques, including Linear Regression, Random Forest, and Gradient Boosting, to model healthcare utilization behavior. Model performance is evaluated using standard regression metrics such as R², RMSE, and MAE, along with cross-validation to assess model stability.

An interactive dashboard was developed to visualize utilization patterns, compare model performance, and dynamically generate predictions based on selected population filters.

Business Problem

Healthcare systems must anticipate patient demand to allocate resources effectively. Unexpected spikes in utilization can lead to:

Increased wait times
Resource shortages
Higher operational costs
Reduced quality of care

By predicting future outpatient visits, healthcare organizations can:

Improve staffing and scheduling decisions
Optimize clinic capacity planning
Identify high-utilization populations
Support preventive care strategies
Research Question

Can demographic, socioeconomic, health status, and prior healthcare utilization data be used to accurately predict Year-2 outpatient office visits?

Dataset

Source:
Medical Expenditure Panel Survey (MEPS)

Panels Used:
Panels 16–20

Population:
Civilian non-institutionalized U.S. population

Sample Size:
Approximately 60,000 patients

Target Variable:
Year-2 Office-Based Visits
OBTOTVY2

Data Preparation

The dataset was cleaned and transformed using Python-based preprocessing workflows.

Key Steps
Merged multi-year MEPS panel data
Selected relevant demographic and clinical variables
Handled missing values using median imputation
Standardized numeric features
Created utilization categories
Removed incomplete records for modeling
Features Used in Modeling
Demographics
Age
Sex
Race
Hispanic Ethnicity
Region
Socioeconomic
Poverty Category
Education Level
Insurance Coverage
Employment Status
Smoking Status
Health Status
Self-Reported Physical Health
Self-Reported Mental Health
Chronic Conditions
Hypertension
Diabetes
Arthritis
Joint Pain
Asthma
Coronary Heart Disease
Heart Attack
Stroke
Emphysema
High Cholesterol
Prior Utilization
Year-1 Office Visits
Models Implemented
1. Linear Regression

Baseline statistical model used to estimate relationships between predictors and healthcare utilization.

Performance

R² ≈ 0.13
RMSE ≈ 74
MAE ≈ 25.9

2. Linear Regression with Cross-Validation

Evaluates model stability across multiple data splits.

Cross-Validation

5-fold cross-validation applied.

Average CV R²

≈ −2.88

3. Random Forest

Ensemble machine learning model capable of capturing nonlinear relationships and feature interactions.

Performance

R² ≈ 0.35
RMSE ≈ 63.9
MAE ≈ 17.8

4. Gradient Boosting

Sequential ensemble model that improves predictive accuracy through iterative error correction.

Performance

R² ≈ 0.45
RMSE ≈ 6.45
MAE ≈ 2.61

Cross-Validation

Average CV R² ≈ 0.27

Model Evaluation Metrics
R² (Coefficient of Determination)

Measures the proportion of variance explained by the model.

RMSE (Root Mean Squared Error)

Measures prediction error magnitude, emphasizing larger errors.

MAE (Mean Absolute Error)

Measures the average absolute difference between predicted and actual values.

Cross-Validation

Evaluates model performance across multiple subsets of data to assess generalization.

Dashboard Features

The interactive dashboard allows users to explore healthcare utilization patterns and model predictions dynamically.

Core Functionality
Model selection dropdown
Real-time prediction updates
Dynamic population filtering
Model performance metrics
Visualization of utilization patterns
Correlation analysis of predictors
Filters
Sex
Region
Insurance Coverage
Age Range
Visualizations
Distribution of Year-2 Visits
Average Visits by Age
Visit Category Distribution
Correlation Matrix
Model Performance Metrics
Technology Stack

Python
Pandas
NumPy
Scikit-learn
Matplotlib
Seaborn
Streamlit
Joblib
