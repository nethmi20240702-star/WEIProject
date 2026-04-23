import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px


# Title
st.title("Water Exploitation Dashboard")

# Description
st.markdown("This dashboard analyzes water stress levels using WEI+ dataset.")

# Load data
df = pd.read_csv("cleaned_wei_data.csv")

# Sidebar
st.sidebar.header("Filters")

country = st.sidebar.selectbox("Select Country", df["Country"].unique())
year = st.sidebar.slider("Select Year",
                         int(df["Year"].min()),
                         int(df["Year"].max()))

quarter = st.sidebar.selectbox("Select Quarter", df["Quarter"].unique())

# Filter data
filtered_df = df[(df["Country"] == country) &
                 (df["Year"] == year) &
                 (df["Quarter"] == quarter)]

# KPI
st.subheader("Key Performance Indicators")

avg_wei = round(filtered_df["WEI"].mean(), 2)
total_consumption = int(filtered_df["Water_Consumption"].sum())
total_abstraction = int(filtered_df["Water_Abstraction"].sum())

col1, col2, col3 = st.columns(3)

col1.metric("Avg WEI (%)", avg_wei)
col2.metric("Total Consumption", total_consumption)
col3.metric("Total Abstraction", total_abstraction)

# Insight
st.info(f"In {year}, {country} has WEI of {avg_wei}%. Higher WEI indicates water stress.")

# Line chart
st.subheader("WEI Trend Over Time")

country_df = df[df["Country"] == country]

yearly_df = country_df.groupby("Year")["WEI"].mean().reset_index()
yearly_df = yearly_df.sort_values("Year")

fig_line = px.line(
    yearly_df,
    x="Year",
    y="WEI",
    title="WEI Trend",
    markers=True
)

st.plotly_chart(fig_line)

# Bar chart 
st.subheader("Quarterly Water Consumption")

# Filter only by country and year (NOT quarter)
bar_df = df[(df["Country"] == country) & (df["Year"] == year)]

fig_bar = px.bar(
    bar_df,
    x="Quarter",
    y="Water_Consumption",
    title="Water Consumption by Quarter",
    color="Quarter"   
)

st.plotly_chart(fig_bar)

# Bar chart 
st.subheader("Top 10 Countries by WEI")

top_df = df[df["Year"] == year].groupby("Country")["WEI"].mean().reset_index()

fig_bar2 = px.bar(
    top_df.sort_values("WEI", ascending=False).head(10),
    x="Country",
    y="WEI",
    title="Top Countries by WEI",
    color="WEI",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_bar2)

# Map
st.subheader("Global Water Stress Map")

map_df = df[df["Year"] == year].groupby("Country")["WEI"].mean().reset_index()

fig_map = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="WEI",
    title="Water Stress Levels by Country",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_map)

# Data table
st.subheader("Filtered Data")
st.write(filtered_df)
