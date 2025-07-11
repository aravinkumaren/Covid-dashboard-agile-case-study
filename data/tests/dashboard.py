import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/covid_19_data.csv", parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

st.title("🌍 COVID-19 Dashboard")
st.markdown("Analyze global COVID-19 trends by country and date")

# Sidebar filters
countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("Select Country", sorted(countries))

min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter dataset
filtered_df = df[(df['Country'] == selected_country) &
                 (df['Date'] >= pd.to_datetime(date_range[0])) &
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# Summary metrics
st.subheader(f"Summary for {selected_country}")
total_cases = int(filtered_df['Confirmed'].sum())
total_deaths = int(filtered_df['Deaths'].sum())
total_recovered = int(filtered_df['Recovered'].sum())

col1, col2, col3 = st.columns(3)
col1.metric("Total Confirmed", f"{total_cases:,}")
col2.metric("Total Deaths", f"{total_deaths:,}")
col3.metric("Total Recovered", f"{total_recovered:,}")

# Line chart
st.subheader("📈 Daily New Cases Over Time")
fig = px.line(filtered_df, x='Date', y='New_cases', title='New Cases Per Day')
st.plotly_chart(fig)

