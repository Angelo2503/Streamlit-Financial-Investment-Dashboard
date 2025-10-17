import streamlit as st
import pandas as pd
import calendar
from utils.data_loader import load_data_modified
from utils.charts_plotly import transactions_quarter_grouped, top_countries_by_units_plot, top_sectors_by_units_plot

# Load data
df = load_data_modified()

st.set_page_config(page_title="Data Analysis", layout="wide")
st.title("📊 Data Analysis")
st.caption("Data source: `symbol.csv` and `account-statement-1-1-2024-12-31-2024.csv`")
st.markdown("🔎 For a full explanation of OLAP operations (e.g. drill-down, roll-up, slice & dice), please refer to the final report.")



#########################
######## QUERY 1 ########
#########################

st.markdown("## Query 1")

st.markdown("#### 🗓️ Filter by Year")
available_years = sorted(df['year'].unique(), reverse=True)
year = st.selectbox("Select Available Year", available_years, index=available_years.index(2024), key="year_q1")

st.markdown(f"### Quarterly Ranking of Transactions in {year} (BUY + SELL)")
fig = transactions_quarter_grouped(df, year)
st.plotly_chart(fig, use_container_width=True)



#########################
######## QUERY 2 ########
#########################

st.markdown("## Query 2")

# Sector filter selection
st.markdown("#### 🏢 Filter by Sector")
available_sector = df['sector'].unique()
sector = st.selectbox("Select Sector", available_sector, index=available_sector.tolist().index("Financial Services"))

# Count the number of countries with transactions in the selected sector
available_countries = df[
    (df['sector'] == sector) & 
    (df['type'] != 'DIVIDENT')
]['country'].nunique()

# Slider to select how many top countries to show
st.markdown("#### 🗺️ Filter by Number of Countries")
threshold = st.slider(
    "Number of Top Countries", 
    min_value=1, 
    max_value=df['country'].nunique(),
    value=5
)

# Title based on the selected filters
st.markdown(f"### Top {threshold} countries by number of units traded in {sector} companies")

# Optional warning (for future-proofing, even if slider already limits input)
if threshold > available_countries:
    st.error(
        f"⚠️ There are only {available_countries} countries available in the '{sector}' sector. "
        f"Please select a threshold equal to or below this number."
    )
else:
    # Generate and display the bar chart and map
    fig_map, fig_bar = top_countries_by_units_plot(df, sector=sector, threshold=threshold)
    st.plotly_chart(fig_map, use_container_width=True, key = 'map_query2')
    st.plotly_chart(fig_bar, use_container_width=True, key = 'bar_query2')



#########################
######## QUERY 3 ########
#########################

st.markdown("## Query 3")

col1, col2 = st.columns(2)

# Select year
with col1:
    st.markdown("#### 🗓️ Filter by Year")
    available_years = sorted(df['year'].unique(), reverse=True)
    year = st.selectbox("Select Available Year", available_years, index=available_years.index(2024),key="year_q3")

# Select Day of Week
with col2:
    st.markdown("#### 📆 Filter by Day of Week")
    giorni = list(calendar.day_name) 
    day_of_week = st.selectbox("Select Day of Week", giorni, index=0)

# Select Type of Transaction
st.markdown("#### 💵 Filter by Type of Transaction")
trans_type = df['type'].unique()
type = st.selectbox("Select Type of Transaction", trans_type, index=1)

# Select threshold
st.markdown("#### 🏢 Filter by Number of Sectors")
threshold = st.slider("Number of Top Sectors", min_value=1, max_value=df['sector'].nunique(), value=3)

# Calcola quanti settori ci sono effettivamente nel giorno selezionato
available_sectors = df[
    (df['year'] == year) &
    (df['day_of_week'] == day_of_week) &
    (df['type'] == type)
]['sector'].nunique()

if available_sectors == 0:
    st.error(f"⚠️ No {type} transactions available for {day_of_week} in {year}. Cannot generate chart.")
else:
    if available_sectors < threshold:
        st.error(f"⚠️ Only {available_sectors} sectors available for {day_of_week} in {year}. Showing all of them.")
        threshold = available_sectors

    st.markdown(f"### Top {threshold} Sectors by Units {type} on {day_of_week} in {year}")
    fig = top_sectors_by_units_plot(df, year=year, day_of_week=day_of_week, type = type, threshold=threshold)
    st.plotly_chart(fig, use_container_width=True)



