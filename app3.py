# ==============================
# IMPORTS
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Healthcare Utilization Dashboard",
    layout="wide"
)

st.title("Healthcare Utilization and Demand Analysis")

st.markdown("---")

# ==============================
# LOAD DATA
# ==============================

@st.cache_data
def load_data():
    return pd.read_csv("meps_dashboard_data.csv")

df = load_data()

# ==============================
# LOAD MODELS
# ==============================

@st.cache_resource
def load_models():

    lr_model = joblib.load(
        "linear_regression_model.pkl"
    )

    lr_cv_model = joblib.load(
        "meps_linear_regression_with_CV.pkl"
    )

    rf_model = joblib.load(
        "meps_random_forest2.pkl"
    )

    gb_model = joblib.load(
        "meps_gradient_boosting.pkl"
    )

    return (
        lr_model,
        lr_cv_model,
        rf_model,
        gb_model
    )


lr_model, lr_cv_model, rf_model, gb_model = load_models()

# ==============================
# LABELS
# ==============================

sex_labels = {
    1: "Male",
    2: "Female"
}

region_labels = {
    1: "Northeast",
    2: "Midwest",
    3: "South",
    4: "West"
}

insurance_labels = {
    1: "Private",
    2: "Public",
    3: "Uninsured"
}

col_labels = {

    "AGE1X": "Age",
    "SEX": "Sex",
    "RACEV1X": "Race",
    "HISPANX": "Hispanic Ethnicity",
    "REGION1": "Region",

    "POVCATY1": "Poverty Category",
    "EDRECODE": "Education Level",
    "INSCOVY1": "Insurance Coverage",
    "EMPST1": "Employment Status",
    "ADSMOK2": "Smoking Status",

    "RTHLTH1": "Self-Reported Physical Health",
    "MNHLTH1": "Self-Reported Mental Health",

    "HIBPDXY1": "Hypertension",
    "DIABDXY1": "Diabetes",
    "ARTHDXY1": "Arthritis",
    "JTPAIN1": "Joint Pain",

    "ASTHDXY1": "Asthma",
    "CHDDXY1": "Coronary Heart Disease",
    "MIDXY1": "Heart Attack",
    "STRKDXY1": "Stroke",

    "EMPHDXY1": "Emphysema",
    "CHOLDXY1": "High Cholesterol",

    "OBTOTVY1": "Year-1 Office Visits"
}

features = list(col_labels.keys())

target = "OBTOTVY2"

# ==============================
# SIDEBAR FILTERS
# ==============================

st.sidebar.header("Dashboard Filters")

sex_filter = st.sidebar.selectbox(
    "Select Sex",
    ["All"] + list(sex_labels.values())
)

region_filter = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(region_labels.values())
)

insurance_filter = st.sidebar.selectbox(
    "Select Insurance",
    ["All"] + list(insurance_labels.values())
)

age_min, age_max = st.sidebar.slider(
    "Select Age Range",
    int(df["AGE1X"].min()),
    int(df["AGE1X"].max()),
    (18, 65)
)

# ==============================
# FILTER DATA
# ==============================

filtered_df = df.copy()

if sex_filter != "All":

    selected_code = [
        k for k, v in sex_labels.items()
        if v == sex_filter
    ][0]

    filtered_df = filtered_df[
        filtered_df["SEX"] == selected_code
    ]

if region_filter != "All":

    selected_region = [
        k for k, v in region_labels.items()
        if v == region_filter
    ][0]

    filtered_df = filtered_df[
        filtered_df["REGION1"] == selected_region
    ]

if insurance_filter != "All":

    selected_insurance = [
        k for k, v in insurance_labels.items()
        if v == insurance_filter
    ][0]

    filtered_df = filtered_df[
        filtered_df["INSCOVY1"] == selected_insurance
    ]

filtered_df = filtered_df[
    (filtered_df["AGE1X"] >= age_min)
    & (filtered_df["AGE1X"] <= age_max)
]

# ==============================
# CREATE VISIT CATEGORY
# ==============================

bins = [-1, 0, 2, 5, 10, 20, float("inf")]

labels = [
    "0 visits",
    "1–2 visits",
    "3–5 visits",
    "6–10 visits",
    "11–20 visits",
    "21+ visits"
]

filtered_df["visit_category"] = pd.cut(
    filtered_df["OBTOTVY2"],
    bins=bins,
    labels=labels
)

# ==============================
# MODEL SELECTION
# ==============================

st.header("Prediction Model Selection")

model_choice = st.selectbox(
    "Select Prediction Model",
    [
        "Linear Regression",
        "Linear Regression with Cross-Validation",
        "Random Forest",
        "Gradient Boosting"
    ]
)

if model_choice == "Linear Regression":
    model = lr_model

elif model_choice == "Linear Regression with Cross-Validation":
    model = lr_cv_model

elif model_choice == "Random Forest":
    model = rf_model

else:
    model = gb_model

# ==============================
# MODEL METRICS (FULL DATA)
# ==============================

model_df = df.dropna(
    subset=features + [target]
)

X_full = model_df[features]
y_full = model_df[target]

y_pred = model.predict(X_full)

r2 = r2_score(y_full, y_pred)

rmse = np.sqrt(
    mean_squared_error(
        y_full,
        y_pred
    )
)

mae = mean_absolute_error(
    y_full,
    y_pred
)

col1, col2, col3 = st.columns(3)

col1.metric("R²", round(r2, 3))
col2.metric("RMSE", round(rmse, 2))
col3.metric("MAE", round(mae, 2))

st.markdown("---")

# ==============================
# PREDICTION SUMMARY
# ==============================

st.header("Prediction Summary")

filtered_clean = filtered_df.dropna(
    subset=features
)

if len(filtered_clean) > 0:

    preds = model.predict(
        filtered_clean[features]
    )

    st.metric(
        "Average Predicted Year-2 Visits",
        round(preds.mean(), 2)
    )

    st.metric(
        "Number of Patients",
        len(filtered_clean)
    )

else:

    st.warning(
        "No data available for selected filters."
    )

# ==============================
# VISUALIZATIONS
# ==============================

st.header("Healthcare Utilization Overview")

col1, col2 = st.columns(2)

with col1:

    fig, ax = plt.subplots(
        figsize=(4, 3)
    )

    ax.hist(
        filtered_df["OBTOTVY2"],
        bins=30
    )

    ax.set_title(
        "Distribution of Year-2 Visits"
    )

    st.pyplot(fig)

with col2:

    age_visits = (
        filtered_df
        .groupby("AGE1X")["OBTOTVY2"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(
        figsize=(4, 3)
    )

    ax.bar(
        age_visits["AGE1X"],
        age_visits["OBTOTVY2"]
    )

    ax.set_title(
        "Average Visits by Age"
    )

    st.pyplot(fig)

# ==============================
# VISIT CATEGORY CHART
# ==============================

st.header(
    "Year-2 Office Visits by Category"
)

visit_counts = (
    filtered_df["visit_category"]
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots(
    figsize=(5, 3)
)

visit_counts.plot(
    kind="bar",
    color="steelblue",
    edgecolor="black",
    ax=ax
)

st.pyplot(fig)

# ==============================
# CORRELATION MATRIX
# ==============================

st.header("Correlation Matrix")

corr_df = filtered_df[
    features
].rename(
    columns=col_labels
)

fig, ax = plt.subplots(
    figsize=(9, 7)
)

sns.heatmap(
    corr_df.corr(),
    cmap="coolwarm",
    annot=True,
    fmt=".2f",
    annot_kws={"size": 5},
    square=True,
    ax=ax
)

st.pyplot(fig)

# ==============================
# FOOTER
# ==============================

st.markdown("---")

st.markdown(
"""
Prepared by: Abhinav Girish  
Course: ALY 6980 — Capstone  
Data Source: Medical Expenditure Panel Survey (MEPS)
"""
)
