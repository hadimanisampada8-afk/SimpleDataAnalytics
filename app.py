import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="🚀 Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("startup_data.csv")
    return df

df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🚀 Startup Analytics Dashboard")
st.markdown("### Funding, Valuation, Revenue & Market Insights")

st.divider()

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

total_startups = len(df)
total_funding = df["Funding Amount (M USD)"].sum()
total_valuation = df["Valuation (M USD)"].sum()
total_revenue = df["Revenue (M USD)"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚀 Startups", total_startups)

with col2:
    st.metric("💰 Funding", f"${total_funding:,.0f}M")

with col3:
    st.metric("📈 Valuation", f"${total_valuation:,.0f}M")

with col4:
    st.metric("💵 Revenue", f"${total_revenue:,.0f}M")

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

industry_filter = st.multiselect(
    "Select Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

filtered_df = df[
    df["Industry"].isin(industry_filter)
]

# --------------------------------------------------
# FUNDING BY INDUSTRY
# --------------------------------------------------

st.subheader("💰 Funding by Industry")

industry_funding = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    industry_funding,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    title="Funding by Industry"
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# VALUATION BY INDUSTRY
# --------------------------------------------------

st.subheader("📈 Valuation by Industry")

industry_val = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    industry_val,
    names="Industry",
    values="Valuation (M USD)",
    title="Valuation Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# FUNDING VS VALUATION
# --------------------------------------------------

st.subheader("🚀 Funding vs Valuation")

fig3 = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Funding vs Valuation"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# REVENUE ANALYSIS
# --------------------------------------------------

st.subheader("💵 Revenue by Industry")

revenue_df = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    revenue_df,
    x="Industry",
    y="Revenue (M USD)",
    color="Industry",
    title="Revenue by Industry"
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# MARKET SHARE
# --------------------------------------------------

st.subheader("🌍 Market Share")

fig5 = px.treemap(
    filtered_df,
    path=["Industry", "Startup Name"],
    values="Market Share (%)",
    title="Market Share Treemap"
)

st.plotly_chart(fig5, use_container_width=True)

# --------------------------------------------------
# TOP STARTUPS
# --------------------------------------------------

st.subheader("🏆 Top Startups by Valuation")

top_startups = filtered_df.sort_values(
    "Valuation (M USD)",
    ascending=False
).head(10)

st.dataframe(
    top_startups,
    use_container_width=True
)

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI Insights")

top_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

top_startup = (
    filtered_df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"Highest funded industry: {top_industry}"
)

st.success(
    f"Highest valuation region: {top_region}"
)

st.success(
    f"Most valuable startup: {top_startup}"
)

st.info(
    "Focus investments on high-growth industries with strong revenue and valuation performance."
)

# --------------------------------------------------
# DATASET PREVIEW
# --------------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    "<center>🚀 Startup Analytics Dashboard | Built with Streamlit & Plotly</center>",
    unsafe_allow_html=True
)
