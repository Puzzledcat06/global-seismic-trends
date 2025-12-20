import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

st.set_page_config(page_title="Global Seismic Trends", layout="wide")

password = quote_plus("Admin@12345")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost/earthquake_db"
)

df = pd.read_sql("SELECT * FROM earthquakes", engine)

st.title("🌍 Global Seismic Trends Dashboard")

st.markdown("Interactive analysis of global earthquake data (2020 – Present)")

# ---------------- Filters ----------------
st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].dropna().unique()),
    default=sorted(df["year"].dropna().unique())
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["country"].dropna().unique()),
    default=[]
)

min_mag, max_mag = st.sidebar.slider(
    "Magnitude Range",
    float(df["mag"].min()),
    float(df["mag"].max()),
    (4.5, float(df["mag"].max()))
)

filtered_df = df[df["year"].isin(year_filter)]
filtered_df = filtered_df[
    (filtered_df["mag"] >= min_mag) &
    (filtered_df["mag"] <= max_mag)
]

if country_filter:
    filtered_df = filtered_df[filtered_df["country"].isin(country_filter)]

# ---------------- Visuals ----------------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        filtered_df,
        x="mag",
        nbins=30,
        title="Magnitude Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        filtered_df,
        names="depth_category",
        title="Depth Category Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    top_countries = (
        filtered_df["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_countries.columns = ["country", "count"]

    fig3 = px.bar(
        top_countries,
        x="country",
        y="count",
        title="Top 10 Earthquake-Prone Countries"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    yearly_counts = (
        filtered_df.groupby("year")
        .size()
        .reset_index(name="count")
    )

    fig4 = px.line(
        yearly_counts,
        x="year",
        y="count",
        markers=True,
        title="Earthquakes Over Time"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("📋 Sample Records")
st.dataframe(filtered_df.head(20))
