import streamlit as st
import pandas as pd
import csv
from datetime import datetime

st.set_page_config(
    page_title="Comparator COT",
    page_icon=":money_with_wings:",
    layout="wide",
)
st.header("Rapport COT")

def Get_dates():
    dates = []
    with open("csv/USD.csv", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for row in reader:
            date = row[0]
            dates.append(date)
    return dates

chosen_date = st.select_slider('Sélectionnez une date', Get_dates())
col1, col2 = st.columns(2)

with col1:
    chosen_currency_1 = st.selectbox('Premier actif', ['USD', 'EUR', 'GBP', 'CHF', 'CAD', 'JPY', 'AUD', 'NZD', 'MXN', 'BRL', 'ZAR', 'BTC', 'ETH', 'OIL', 'GAS', 'WHEAT', 'GOLD', 'SILVER', 'COPPER', 'S&P 500', 'NASDAQ-100', 'DOW JONES'])
    chosen_file_name_1 = "csv/" + chosen_currency_1 + ".csv"

with col2:
    chosen_currency_2 = st.selectbox('Deuxième actif', ['USD', 'EUR', 'GBP', 'CHF', 'CAD', 'JPY', 'AUD', 'NZD', 'MXN', 'BRL', 'ZAR', 'BTC', 'ETH', 'OIL', 'GAS', 'WHEAT', 'GOLD', 'SILVER', 'COPPER', 'S&P 500', 'NASDAQ-100', 'DOW JONES'])
    chosen_file_name_2 = "csv/" + chosen_currency_2 + ".csv"

dates_1 = []
change_long_1 = []
change_short_1 = []
net_position_1 = []
data_1 = []

with open(chosen_file_name_1, newline="") as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)
    for row in reader:
        date = row[0]
        dates_1.append(date)
        change_long_value = int(row[3])
        change_short_value = int(row[4])
        net_position_value = int(row[5])

        change_long_1.append(change_long_value)
        change_short_1.append(change_short_value)
        net_position_1.append(net_position_value)
        
        data_1.append([date, change_long_value, change_short_value, net_position_value])
        if date == chosen_date:
            break

dates_2 = []
change_long_2 = []
change_short_2 = []
net_position_2 = []
data_2 = []

with open(chosen_file_name_2, newline="") as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)

    for row in reader:
        date = row[0]
        dates_2.append(date)
        change_long_value = int(row[3])
        change_short_value = int(row[4])
        net_position_value = int(row[5])

        change_long_2.append(change_long_value)
        change_short_2.append(change_short_value)
        net_position_2.append(net_position_value)
        
        data_2.append([date, change_long_value, change_short_value, net_position_value])
        if date == chosen_date:
            break

def format_value(value):
    color = "red" if value < 0 else "green"
    return "color: %s" % color

df_1 = pd.DataFrame(data_1, columns=["Date", "Change long", "Change short", "Net position"])
df_1_styled = df_1.style.applymap(format_value, subset=["Change long", "Change short", "Net position"])

df_2 = pd.DataFrame(data_2, columns=["Date", "Change long", "Change short", "Net position"])
df_2_styled = df_2.style.applymap(format_value, subset=["Change long", "Change short", "Net position"])

with col1:
    st.header(chosen_currency_1)
    st.dataframe(df_1_styled, hide_index=True, use_container_width=True, height=len(df_1) * 36)

with col2:
    st.header(chosen_currency_2)
    st.dataframe(df_2_styled, hide_index=True, use_container_width=True, height=len(df_2) * 36)