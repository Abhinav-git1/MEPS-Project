import streamlit as st
from PIL import Image

# --------------------------------
# PASSWORD PROTECTION
# --------------------------------

def check_password():

    def password_entered():
        if st.session_state["password"] == "MEPS2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:

        st.title("Private Dashboard Access")

        st.text_input(
            "Enter password",
            type="password",
            on_change=password_entered,
            key="password"
        )

        st.stop()

    elif not st.session_state["password_correct"]:

        st.title("Private Dashboard Access")

        st.text_input(
            "Enter password",
            type="password",
            on_change=password_entered,
            key="password"
        )

        st.error("Incorrect password")

        st.stop()

    return True


check_password()

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="MEPS Healthcare Utilization Dashboard",
    layout="wide"
)

# --------------------------------
# TITLE
# --------------------------------

st.markdown(
    "<h1 style='text-align: center;'>Healthcare Utilization and Demand Analysis</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>Medical Expenditure Panel Survey (MEPS)</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>Prepared by: Abhinav Girish</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------
# FUNCTION TO DISPLAY CLICKABLE CHART
# --------------------------------

def show_clickable_chart(title, filename, explanation):

    with st.expander(title):

        image = Image.open(filename)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image(
                image,
                width=650
            )

        st.markdown("")

        st.markdown(
            f"""
**Interpretation:**  
{explanation}
"""
        )

        st.markdown("---")

# =================================
# DISTRIBUTION ANALYSIS
# =================================

st.header("Distribution Analysis")

show_clickable_chart(
    "Figure 1: Distribution of Year-2 Office-Based Visits",
    "figure_1_distribution_visits.png",
    "Most individuals had zero physician visits, while a small group had very high utilization."
)

show_clickable_chart(
    "Figure 2: Distribution of Chronic Condition Count",
    "figure_2_chronic_count.png",
    "Most individuals had zero or one chronic condition."
)

show_clickable_chart(
    "Figure 3: Top Conditions by Average Year-2 Physician Visits",
    "figure_3_top_conditions.png",
    "Certain chronic conditions are associated with higher physician visit frequency."
)

# =================================
# DEMOGRAPHIC PATTERNS
# =================================

st.header("Demographic and Health Patterns")

show_clickable_chart(
    "Figure 4: Chronic Condition Prevalence by Age Group",
    "figure_4_chronic_by_age.png",
    "Chronic condition prevalence increases with age."
)

show_clickable_chart(
    "Figure 5: Average Physical and Mental Health Status by Race",
    "figure_5_health_by_race.png",
    "Self-reported health status varies across racial groups."
)

show_clickable_chart(
    "Figure 6: Prevalence of Chronic Condition by Race",
    "figure_6_chronic_by_race.png",
    "Chronic conditions differ across racial groups."
)

show_clickable_chart(
    "Figure 7: Education Level Distribution by Hispanic Ethnicity",
    "figure_7_education_hispanic.png",
    "Education levels vary across Hispanic and non-Hispanic populations."
)

show_clickable_chart(
    "Figure 8: Poverty Level Distribution by Hispanic Ethnicity",
    "figure_8_poverty_hispanic.png",
    "Socioeconomic differences are visible across ethnicity groups."
)

# =================================
# UTILIZATION PATTERNS
# =================================

st.header("Healthcare Utilization Patterns")

show_clickable_chart(
    "Figure 9: Age Group vs Average Physician Visits",
    "figure_9_age_visits.png",
    "Healthcare utilization increases with age."
)

show_clickable_chart(
    "Figure 10: Sex vs Average Physician Visits",
    "figure_10_sex_visits.png",
    "Utilization differs slightly between males and females."
)

show_clickable_chart(
    "Figure 11: Race vs Average Physician Visits",
    "figure_11_race_visits.png",
    "Utilization varies across racial groups."
)

show_clickable_chart(
    "Figure 12: Region vs Average Physician Visits",
    "figure_12_region_visits.png",
    "Regional variation in healthcare utilization is observed."
)

# =================================
# MODELING INSIGHTS
# =================================

st.header("Predictive Modeling Insights")

show_clickable_chart(
    "Figure 13: Top Predictors of Year-2 Office Visits",
    "figure_13_feature_importance.png",
    "Prior utilization and chronic conditions are strong predictors."
)

show_clickable_chart(
    "Figure 14: Correlation Matrix of Predictors",
    "figure_14_correlation_matrix.png",
    "Predictors show mostly low to moderate correlation."
)

show_clickable_chart(
    "Figure 15: SHAP Feature Importance",
    "figure_15_shap_importance.png",
    "SHAP analysis confirms the most influential predictors."
)

show_clickable_chart(
    "Figure 16: Predicted vs Actual Year-2 Outpatient Visits (Final Model)",
    "figure_16_predicted_vs_actual_visits.png",
    "This chart compares predicted and actual Year-2 outpatient visits. Points close to the diagonal line indicate accurate predictions. The model predicts typical utilization well but is less precise for very high utilization cases. This pattern is consistent with the model’s performance metrics, including an R² of approximately 0.46 and a cross-validated R² of approximately 0.43."
)

# =================================
# MODEL EVALUATION
# =================================

st.header("Model Evaluation")

with st.expander("Understanding Model Performance Metrics"):

    st.markdown(
"""
Model performance was evaluated using standard regression metrics and cross-validation to assess predictive accuracy and model reliability.

---

### Model 1: Linear Regression (Baseline Model)

R² = **0.13**  
RMSE = **74.01**  
MAE = **25.91**

The linear regression model served as the baseline model and provided an initial estimate of healthcare utilization. While the model captured general utilization trends, its performance was limited due to the complex and nonlinear nature of healthcare demand.

---

### Linear Regression Cross-Validation Results

Cross-Validation R² Scores:

-13.62  
0.10  
0.04  
-0.12  
-0.79  

Average Cross-Validation R² = **-2.88**

The negative cross-validation results indicated that the linear regression model struggled to generalize across different data samples. This instability reflects the highly variable and skewed nature of healthcare utilization data and highlighted the need for more flexible modeling approaches.

---

### Model 2: Random Forest (Improved Model)

R² = **0.35**

The Random Forest model improved predictive performance by capturing nonlinear relationships among demographic characteristics, chronic conditions, and prior healthcare utilization.

---

### Model 3: Random Forest with Log Transformation (Final Model)

R² = **0.46**  
Cross-Validation R² = **0.43**

Applying a log transformation to the target variable stabilized model performance and produced the best predictive accuracy. The final Random Forest model demonstrated strong generalization across data samples and provided the most reliable predictions of Year-2 outpatient visits.

---

### Overall Interpretation

Model performance improved progressively as more advanced modeling techniques were introduced. The transition from Linear Regression to Random Forest and then to a log-transformed Random Forest model demonstrates the importance of handling skewed healthcare utilization data and capturing nonlinear relationships in healthcare demand.
"""
    )

st.markdown("---")

# --------------------------------
# FOOTER
# --------------------------------

st.markdown(
"""
**Prepared by:** Abhinav Girish  
**Course:** ALY 6980 — Capstone  
**Data Source:** Medical Expenditure Panel Survey (MEPS)  
**Tools:** Python, Streamlit, Machine Learning
"""
)
