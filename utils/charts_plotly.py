import plotly.graph_objects as go
import plotly.express as px
from matplotlib import cm, colors as mcolors
import pandas as pd


# used in LandingPage.py for show companies sector

def plot_companies_by_sector(df):
    """
    Create a horizontal bar chart showing the number of companies per sector.

    Parameters:
        df (pd.DataFrame): A DataFrame containing at least a 'sector' column.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure displaying a bar chart.

    Notes:
        - Each bar represents a sector and its corresponding number of companies.
        - Sectors labeled as 'unknown' (used to replace missing values) are colored gray (#837783),
          while all other sectors are colored purple (#970294).
    """
    # Filter data
    sector_counts = df['sector'].value_counts().sort_values(ascending=True)
    
    # Colors
    colors = ['#837783' if sector == 'unknown' else '#970294' for sector in sector_counts.index]

    fig = go.Figure()
    
    # bar chart
    fig.add_trace(go.Bar(
        y=sector_counts.index,
        x=sector_counts.values,
        orientation='h',
        marker_color=colors,
        text=[str(int(val)) for val in sector_counts.values],
        textposition='auto'
    ))

    fig.update_layout(
        title='Number of Companies by Sector',
        xaxis_title='Number of Companies',
        yaxis_title='Sector',
        height=500,
        template='simple_white'
    )

    return fig


# used in 1_Query.py for Query 1

def transactions_quarter_grouped(df, year = 2024):
    """
    Build an interactive Plotly bar chart that compares the number of BUY and SELL
    transactions per quarter. Quarters are sorted from the most to the least active
    based on the combined total (BUY + SELL).

    Parameters:
    - df (DataFrame): The input DataFrame containing transaction data.
    - year (int): The year to filter the data by (default is 2024).

    Returns:
    - fig (plotly.graph_objects.Figure): Interactive grouped bar chart ready for display.
    """

    # Filter data
    transactions = (
        df[(df["year"] == year) & (df["type"] != 'DIVIDENT')]
        .groupby(["quarter", "type"])
        .size()                         
    )

    # Pivot into a wide table
    by_quarter = transactions.unstack(fill_value=0)

    # Sort quarters by total transactions (BUY + SELL)
    totals = by_quarter.sum(axis=1)                      
    by_quarter = by_quarter.loc[totals.sort_values(ascending=False).index]

    # compute percentage labels
    pct_buy  = (by_quarter["BUY"]  / totals * 100).round(1).astype(str) + "%"
    pct_sell = (by_quarter["SELL"] / totals * 100).round(1).astype(str) + "%"
    
    # Build the grouped-bar figure
    quarters_lbl = [f"Q{q}" for q in by_quarter.index]
    fig = go.Figure()
    
    # BUY bars
    fig.add_bar(
        x=quarters_lbl,
        y=by_quarter["BUY"],
        name="BUY",
        marker_color="#7197F9",
        text=pct_buy,
        textposition="auto",          
        insidetextanchor="start",       
        textfont=dict(color="white")    
    )

    # SELL bars
    fig.add_bar(
    x=quarters_lbl,
    y=by_quarter["SELL"],
    name="SELL",
    marker_color="#FFA04C",
    text=pct_sell,
    textposition="inside",
    insidetextanchor="start",
    textfont=dict(color="white")
    )
    
    # Add label 
    for q_lbl, (buy, sell) in zip(quarters_lbl, by_quarter[["BUY", "SELL"]].itertuples(index=False)):
        total   = buy + sell
        highest = max(buy, sell)
        fig.add_annotation(
            x=q_lbl,
            y=highest,
            text=str(total),
            showarrow=False,
            yshift=8,                   
            font=dict(size=12, color="#000000")
        )

    # layout
    fig.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Number of Transactions",
        barmode="group",             
        bargap=0.5,
        template="simple_white",
        height=500,
        width=800,
        legend_title_text="Type",
    )

    return fig


# used in 1_Query.py for Query 2

def top_countries_by_units_plot(df, sector='Financial Services', threshold=5):
    """
    Generates a choropleth map and a horizontal bar chart showing the top countries 
    by total units traded in the selected sector. Countries labeled as 'Unknown' 
    are included in the bar chart (with neutral color) but excluded from the map 
    as they cannot be geographically located.

    Parameters:
    - df (DataFrame): The input DataFrame containing transaction data, with columns 
      including 'sector', 'country', and 'unit'.
    - sector (str): The sector to filter transactions by (default is 'Financial Services').
    - threshold (int): The number of top countries (by total units) to display (default is 5).

    Returns:
    - fig_map (plotly.graph_objects.Figure): A choropleth map highlighting the top countries,
      excluding 'Unknown'.
    - fig_bar (plotly.graph_objects.Figure): A horizontal bar chart of the top countries,
      including 'Unknown' if present.
    """

    # Change country names that are not recognized by Plotly
    country_name_map = {
        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
        'United States of America': 'United States',
        'Netherlands, Kingdom of the': 'Netherlands',
        'Virgin Islands (British)': 'British Virgin Islands',
        'Cayman Islands': 'Cayman Islands',
        'unknown': 'Unknown'
    }

    # Apply the name mapping to a clean country column
    df['country_clean'] = df['country'].replace(country_name_map)

    # Filter data
    countries = (
        df[df['sector'] == sector]
        .groupby('country_clean')['unit']
        .sum()
        .sort_values(ascending=True)
    )

    top_countries = countries.tail(threshold)

    # Exclude 'Unknown' from the map visualization
    visible_countries = top_countries.drop(labels=[
        c for c in top_countries.index if c == "Unknown"
    ])

    # Mapping colors to each country
    cmap = cm.get_cmap("tab20")
    color_map = {
        country: mcolors.to_hex(cmap(i % cmap.N))
        for i, country in enumerate(visible_countries.index)
    }

    # Assign a neutral color to 'Unknown' if present
    for c in top_countries.index:
        if c not in color_map:
            color_map[c] = '#837783'

    # map 
    map_df = pd.DataFrame({
        'country': visible_countries.index,
        'unit': visible_countries.values
    })

    fig_map = px.choropleth(
        map_df,
        locations='country',
        locationmode='country names',
        color='country',
        hover_name='country',
        projection='natural earth',
        color_discrete_map=color_map
    )
    fig_map.update_traces(marker_line_width=0.5, marker_line_color="white")
    fig_map.update_layout(
        legend_title_text='Country',
        coloraxis_showscale=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )

    # bar chart 
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=top_countries.index,
        x=top_countries.values,
        orientation='h',
        marker_color=[color_map[c] for c in top_countries.index],
        marker_line_width=0.5,
        text=[str(int(val)) for val in top_countries.values],
        textposition='auto'
    ))
    fig_bar.update_layout(
        xaxis_title='Total Units Traded',
        yaxis_title='Country',
        template='simple_white',
        bargap=0.5,
        height=500,
        width=800,
        margin=dict(t=50, b=50, l=100, r=50)
    )

    # mean
    mean = countries.mean()
    fig_bar.add_vline(
        x=mean,
        line_dash="dash",
        line_color="#2E2E2E",
        line_width=2,
        annotation_text=f"<b>{sector}<br>Mean: {mean:.0f}</b>",
        annotation_position="bottom right",
        annotation_font_color="#2E2E2E"
    )

    return fig_map, fig_bar


# used in 1_Query.py for Query 3

def top_sectors_by_units_plot(df, year=2024, day_of_week='Monday', type = 'SELL', threshold=3):

    """
    Creates a horizontal Plotly bar chart showing the top sectors by total units 
    sold on a specific day of the week in a given year.

    Parameters:
    - df (DataFrame): The input DataFrame containing transaction data.
    - year (int): The year to filter the data by (default is 2024).
    - day_of_week (str): Day of the week to filter by (default is 'Monday').
    - threshold (int): Number of top sectors to show (default is 3).

    Returns:
    - fig (plotly.graph_objects.Figure): The resulting Plotly bar chart.
    """

    # Filter data
    sectors = (
        df[
            (df['day_of_week'] == day_of_week) &
            (df['year'] == year) &
            (df['type'] == type)
        ]
        .groupby('sector')['unit']
        .sum()
        .sort_values(ascending=True)
    )

    top_sectors = sectors.tail(threshold)

    fig = go.Figure()

    colors = ['#837783' if str(cat).lower() == 'unknown' else '#008B8B' for cat in top_sectors.index]

    # bar chart
    fig.add_trace(go.Bar(
        y=top_sectors.index,
        x=top_sectors.values,
        orientation='h',
        marker_color=colors,
        text=[str(int(val)) for val in top_sectors.values],
        textposition='auto'
    ))


    fig.update_layout(
        xaxis_title=f'Total Units ({type})',
        yaxis_title='Sector',
        template='simple_white',
        bargap=0.5,
        height=500,
        width=800,
        margin=dict(t=50, b=50, l=100, r=50)
    )

    # Mean
    if sectors.nunique() > 1:
        mean = sectors.mean()
        fig.add_vline(
            x=mean,
            line_dash="dash",
            line_color="#2E2E2E",
            line_width=2,
            annotation_text=f"<b>{day_of_week} {year}<br>Mean: {mean:.0f}</b>",
            annotation_position="bottom right",
            annotation_font_color="#2E2E2E"
        )

    return fig


# used in 2_TimeAnalysis.py for all bar charts

def plot_top_categories(df, group_by_field, threshold=5, map_sector=False, color="#3878A5"):
    """
    Generate an interactive horizontal bar chart displaying the top-N categories
    (by transaction count) for a chosen column of the dataset.

    Parameters:
    - df (DataFrame): The input DataFrame containing transaction data.
    - group_by_field (str): Column name to aggregate by, e.g. "symbol", "sector", or "industry".
    - threshold (int): Number of top categories to show (default is 5).
    - map_sector (bool): If True, colour bars by 'sector' and show legend.
    - color (str): HEX colour code used when map_sector is False.

    Returns:
    - plotly.graph_objects.Figure: Interactive bar chart.
    """

    # Mapping symbol → company_name
    if group_by_field == "symbol" and "company_name" in df.columns:
        symbol_to_name = (
            df.drop_duplicates("symbol")
              .set_index("symbol")["company_name"]
              .to_dict()
        )
    else:
        symbol_to_name = {}

    if map_sector:
        data = (
            df[[group_by_field, 'sector']]
            .value_counts()
            .sort_values(ascending=False)
            .head(threshold)
            .reset_index(name="count")
        )
    else:
        data = (
            df[group_by_field]
            .value_counts()
            .sort_values(ascending=False)
            .head(threshold)
            .reset_index(name="count")
        )

    # Etichetta: company name (symbol) se group_by_field = symbol
    if group_by_field == "symbol" and symbol_to_name:
        data["label"] = data[group_by_field].map(
            lambda sym: f"{symbol_to_name.get(sym, sym)} ({sym})"
        )
    else:
        data["label"] = data[group_by_field]

    fig = go.Figure()

    if map_sector:
        unique_sectors = data["sector"].unique()
        tab20 = cm.get_cmap("tab20")
        sector_color_map = {
            sec: mcolors.to_hex(tab20(i % tab20.N))
            for i, sec in enumerate(unique_sectors)
        }

        for sec in unique_sectors:
            mask = data["sector"] == sec
            fig.add_bar(
                x=data.loc[mask, "count"],
                y=data.loc[mask, "label"],
                orientation="h",
                marker_color=sector_color_map[sec] if not (data.loc[mask, "label"] == 'unknown').all() else "#837783",
                marker_line_width=0.5,
                text=data.loc[mask, "count"],
                textposition="auto",
                name=sec
            )
    else:
        colors = ['#837783' if str(label).lower() == 'unknown' else color for label in data["label"]]

        fig.add_bar(
            x=data["count"],
            y=data["label"],
            orientation="h",
            marker_color=colors,
            marker_line_width=0.5,
            text=data["count"],
            textposition="auto",
            showlegend=False
        )


    fig.update_layout(
        xaxis_title="Transaction Count",
        yaxis_title="Company" if group_by_field == "symbol" else group_by_field.capitalize(),
        height=500,
        bargap=0.5,
        margin=dict(l=120, r=40, t=30, b=40),
        template="simple_white",
        showlegend=True if map_sector else False,
        legend_title_text="Sector" if map_sector else "",
        yaxis=dict(categoryorder="total ascending")
    )

    return fig
