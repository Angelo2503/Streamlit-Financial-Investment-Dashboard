import streamlit as st
from PIL import Image

st.set_page_config(page_title="Star Schema", layout="wide")

st.title("⭐ Star Schema Overview")

##############################
##### Star Schema Intro ######
##############################

st.markdown("""
This page presents the **Star Schema** designed for this analytical project.  
It organizes the data into one central fact table and several surrounding dimension tables, 
enabling efficient queries for business intelligence, KPI tracking, and dashboarding.
""")

st.markdown("📄 For a detailed explanation of the star schema and its rationale, please refer to the final report.")

##############################
##### Schema Visualization ###
##############################

st.subheader("📊 Star Schema Diagram")

# Load and display image
image = Image.open("./files/star_schema.drawio.png")  # Update path if needed
st.image(image, use_container_width=True)

##############################
##### Tables Explanation #####
##############################

st.markdown("""
### 🧩 Components

#### 📦 Fact Table: `fact_TRANSACTION`
Stores measurable events (facts) such as transaction volumes. Includes:
- `transaction_id` (primary key)
- `time_id` → links to `dim_TIME`
- `geography_id` → links to `dim_GEOGRAPHY`
- `symbol_id` → links to `dim_SYMBOL`
- `transaction_type_id` → links to `dim_TRANSACTION_TYPE`
- `unit` → quantity traded

---

#### 🕒 Dimension Table: `dim_TIME`
Describes the temporal context of each transaction:
- `time_id` (surrogate key)
- `day_of_week`
- `quarter`
- `year`

---

#### 🌍 Dimension Table: `dim_GEOGRAPHY`
Provides geographic context:
- `geography_id` (surrogate key)
- `country`

---

#### 🏢 Dimension Table: `dim_SYMBOL`
Provides company-level metadata:
- `symbol_id` (surrogate key)
- `symbol`
- `company_name`
- `sector`
- `industry`

---

#### 💰 Dimension Table: `dim_TRANSACTION_TYPE`
Defines the nature of the transaction:
- `transaction_type_id` (surrogate key)
- `transaction_type` → e.g., `BUY`, `SELL`, `DIVIDENT`

---

""")
