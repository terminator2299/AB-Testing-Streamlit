# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ab_core import tracking, analysis

st.set_page_config(page_title="A/B Testing Framework", layout="centered")

st.title("🧪 A/B Testing Framework")
st.write("Simulate or analyze A/B experiments using synthetic or uploaded data.")

# --------------------------------------------
# Section 1: Simulate Experiment
# --------------------------------------------
st.markdown("### 🎯 Simulate A/B Test")

with st.form("simulate_form"):
    variants_input = st.text_input("Enter variants (comma-separated)", value="A,B")
    variants = [v.strip() for v in variants_input.split(",") if v.strip()]
    num_users = st.slider("Number of users to simulate", 100, 10000, 1000)

    st.markdown("#### Conversion Rates for Variants")
    conversion_rates = {}
    for v in variants:
        conversion_rates[v] = st.slider(f"Conversion rate for {v}", 0.0, 1.0, 0.1, step=0.01)

    simulate_btn = st.form_submit_button("Run Simulation")

if simulate_btn:
    df = tracking.simulate_events(num_users, variants, conversion_rates)
    st.success("✅ Simulation complete!")

    st.markdown("#### 📄 Sample Data")
    st.dataframe(df.head(), use_container_width=True)

    summary, p_value = analysis.analyze(df)

    st.markdown("#### 📊 Summary")
    st.dataframe(summary)

    st.markdown(f"**P-Value:** `{p_value:.4f}`")
    if p_value < 0.05:
        st.success("Statistically significant difference between variants.")
    else:
        st.info("No statistically significant difference found.")

    st.markdown("#### 📉 Conversion Rate Chart")
    fig, ax = plt.subplots()
    ax.bar(summary["variant"], summary["Conversion Rate"], color="royalblue")
    ax.set_ylabel("Conversion Rate")
    ax.set_title("Conversion Rate by Variant")
    st.pyplot(fig)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Simulated Data", csv, "simulated_data.csv", "text/csv")

# --------------------------------------------
# Section 2: Upload CSV Data
# --------------------------------------------
st.markdown("---")
st.markdown("### 📤 Upload Your Own Experiment Data")

uploaded_file = st.file_uploader("Upload CSV with columns: user_id, variant, converted", type="csv")

if uploaded_file:
    try:
        df_uploaded = pd.read_csv(uploaded_file)

        if {"user_id", "variant", "converted"}.issubset(df_uploaded.columns):
            st.success("✅ File uploaded successfully!")
            st.dataframe(df_uploaded.head(), use_container_width=True)

            summary, p_value = analysis.analyze(df_uploaded)

            st.markdown("#### 📊 Summary")
            st.dataframe(summary)

            st.markdown(f"**P-Value:** `{p_value:.4f}`")
            if p_value < 0.05:
                st.success("Statistically significant difference between variants.")
            else:
                st.info("No statistically significant difference found.")

            st.markdown("#### 📉 Conversion Rate Chart")
            fig, ax = plt.subplots()
            ax.bar(summary["variant"], summary["Conversion Rate"], color="darkorange")
            ax.set_ylabel("Conversion Rate")
            ax.set_title("Conversion Rate by Variant (Uploaded Data)")
            st.pyplot(fig)
        else:
            st.error("CSV must contain: user_id, variant, converted")

    except Exception as e:
        st.error(f"Error loading file: {e}")
