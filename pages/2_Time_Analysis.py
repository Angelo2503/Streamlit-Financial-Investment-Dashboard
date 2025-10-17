import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data_modified
from utils.charts_plotly import plot_top_categories

st.set_page_config(page_title="Time Analysis", layout="wide")
st.title("📈 Time Analysis of Transactions")
st.caption("Data source: `symbol.csv` and `account-statement-1-1-2024-12-31-2024.csv`")

# Load data
df = load_data_modified()

################################
### Filter by Quarter & Year ###
################################
st.markdown("## 🗓️ Filter by Quarter Range")

available_quarters = sorted(df['quarter'].unique())  # [1, 2, 3, 4]
available_years = sorted(df['year'].unique())

col1, col2, col3, col4 = st.columns(4)
with col1:
    start_quarter = st.selectbox("Start Quarter", available_quarters, index=0)
with col2:
    start_year = st.selectbox("Start Year", available_years, index=available_years.index(2024))
with col3:
    end_quarter = st.selectbox("End Quarter", available_quarters, index=3)
with col4:
    end_year = st.selectbox("End Year", available_years, index=available_years.index(2024))


if start_year > end_year or (start_year == end_year and start_quarter > end_quarter):
    st.error("🚫 Start quarter must be before or equal to end quarter.")
else:
    filtered_df = df[
        (
            (df['year'] > start_year) |
            ((df['year'] == start_year) & (df['quarter'] >= start_quarter))
        ) &
        (
            (df['year'] < end_year) |
            ((df['year'] == end_year) & (df['quarter'] <= end_quarter))
        ) &
        (df['type'] != 'DIVIDENT')
    ]

    st.markdown(f"### Transactions from Q{start_quarter} {start_year} to Q{end_quarter} {end_year} (BUY + SELL)")

    if filtered_df.empty:
        st.error("⚠️ No transactions found in selected period.")
    else:

        filtered_df["period"] = filtered_df["year"].astype(str) + "-Q" + filtered_df["quarter"].astype(str)

        line_data = (
            filtered_df
            .groupby("period")
            .size()
            .reset_index(name="transaction_count")
            .sort_values("period")
        )

        fig_line = px.line(
            line_data,
            x="period",
            y="transaction_count",
            markers=True
        )

        fig_line.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Transaction Count",
            template="simple_white",
            height=400,
            margin=dict(t=10, b=40, l=60, r=30)
        )

        st.plotly_chart(fig_line, use_container_width=True)

        #######################
        ### Symbol Analysis ###
        #######################
        st.markdown("#### 💹 Filter by Number of Companies")
        
        symbol_threshold = st.slider("Top Symbols", 1, df['symbol'].nunique(), 3)
        st.markdown(f"### Top {symbol_threshold} Traded Symbols")
        
        map_by_sector = st.checkbox("Color by Sector", value=True, key="map_sector1")
        
        available_symbols = filtered_df['symbol'].nunique()
        if symbol_threshold > available_symbols:
            st.error(f"⚠️ Only {available_symbols} symbols available in the selected period.")
        else:
            fig_symbols = plot_top_categories(
                df=filtered_df,
                group_by_field='symbol',
                threshold=symbol_threshold,
                map_sector=map_by_sector
            )
            st.plotly_chart(fig_symbols, use_container_width=True)

        #######################
        ### Sector Analysis ###
        #######################
        st.markdown("#### 🏢 Filter by Number of Sectors")
        sector_threshold = st.slider("Top Sectors", 1, df['sector'].nunique(), 5)
        st.markdown(f"### Top {sector_threshold} Sectors")
        available_sectors = filtered_df['sector'].nunique()
        if sector_threshold > available_sectors:
            st.error(f"⚠️ Only {available_sectors} sectors available.")
        else:
            fig_sectors = plot_top_categories(
                df=filtered_df,
                group_by_field='sector',
                threshold=sector_threshold,
                color="#556B2F"
            )
            st.plotly_chart(fig_sectors, use_container_width=True)

        #########################
        ### Industry Analysis ###
        #########################
        st.markdown("#### 🏭 Filter by Number of Industries")
        industry_threshold = st.slider("Top Industries", 1, df['industry'].nunique(), 5)
        st.markdown(f"### Top {industry_threshold} Industries")
        map_by_sector2 = st.checkbox("Color by Sector", value=True, key="map_sector2")
        available_industries = filtered_df['industry'].nunique()
        if industry_threshold > available_industries:
            st.error(f"⚠️ Only {available_industries} industries available.")
        else:
            fig_industries = plot_top_categories(
                df=filtered_df,
                group_by_field='industry',
                threshold=industry_threshold,
                map_sector=map_by_sector2
            )
            st.plotly_chart(fig_industries, use_container_width=True)
