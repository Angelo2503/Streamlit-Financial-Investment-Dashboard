import pandas as pd
import streamlit as st

@st.cache_data
def load_data_modified():
    # EXTRACT
    df_symbols = pd.read_csv('./data/symbols.csv', sep=';')
    df_acc_stat = pd.read_csv('./data/account-statement-1-1-2024-12-31-2024.csv', sep=';')
    
    # TRANSFORMATION
    
    # drop useless column 
    df_acc_stat = df_acc_stat.drop(columns=['Unnamed: 5'])
    
    # drop row with all null values
    df_acc_stat = df_acc_stat.dropna()
    
    # rewrite name of columns
    df_acc_stat.columns = [
        "transaction_id",   
        "date", 
        "type",             
        "symbol",   
        "unit"
    ]

    # split the date column and add quarter and day of week
    df_acc_stat['date'] = pd.to_datetime(df_acc_stat['date'], format="%d/%m/%Y %H:%M:%S")

    df_acc_stat['year'] = df_acc_stat['date'].dt.year

    df_acc_stat['quarter'] = df_acc_stat['date'].dt.quarter

    df_acc_stat['day_of_week'] = df_acc_stat['date'].dt.day_name()

    # remove the original date column
    df_acc_stat = df_acc_stat.drop(columns=['date'])
    
    # LEFT join 
    df_trans = pd.merge(df_acc_stat, df_symbols, on='symbol', how='left')

    # after LEFT join replace null values in ''company_name', 'sector', 'industry', 'country' columns with 'unknown' (9.29 % of data)
    df_trans[['company_name', 'sector', 'industry', 'country']] = df_trans[['company_name', 'sector', 'industry', 'country']].fillna('unknown')

    # LOAD
    return df_trans





