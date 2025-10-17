import streamlit as st
from utils.data_loader import load_data_modified
from utils.charts_plotly import plot_companies_by_sector

st.set_page_config(page_title="📊 Investment Dashboard", layout="wide")

###############################
##### Dashboard Header ########
###############################

st.title("📊 Investment Transactions Dashboard")
st.caption("Data source: `symbol.csv` and `account-statement-1-1-2024-12-31-2024.csv`")

st.markdown("""
Welcome to the interactive dashboard for exploring investment transaction data!

This app allows you to:
- Explore a **Star Schema**-based structure for analytical insights  
- Execute dynamic **OLAP-style queries**  
- Perform **time-based analysis** of transactions with custom filters  

👈 Use the **menu** on the left to navigate through the different analytical pages and  
👇 click the button below to **download the full report**.
""")


# Download report
with open("./files/Homework3_Report.pdf", "rb") as f:
    st.download_button(
        label="📥 **Download Full Report**",
        data=f,
        file_name="Homework3_Report.pdf",
        mime="application/pdf"
    )

###############################
##### Load & Preview Data #####
###############################

df = load_data_modified()

# Optional overview visualization
st.subheader("🏢 Company Distribution by Sector")
fig = plot_companies_by_sector(df)
st.plotly_chart(fig, use_container_width=True)

# Percentage of unknowns
percentage = (len(df[df.sector == 'unknown']) / len(df)) * 100
st.info(
    f"The **'unknown'** sector represents a significant portion: **{percentage:.2f}%**  \n"
    "➡️ Go to the **Time Analysis** page to explore transaction trends by date and category."
)
