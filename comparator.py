import streamlit as st
import pandas as pd
import csv

st.header("Rapport COT")

dates = []
change_long = []
change_short = []
net_position = []
data = []

chosen_currency = st.selectbox('Selectionne un actif', ['EUR', 'USD', 'AUD', 'BRL', 'BTC', 'CAD', 'CHF', 'COPPER', 'DOW JONES', 'ETH', 'GAS', 'GBP', 'GOLD', 'JPY', 'MXN', 'NASDAQ', 'NZD', 'OIL', 'S&P 500', 'SILVER', 'ZAR'])
chosen_file_name = "csv/" + chosen_currency + "_27-06-23.csv"

with open(chosen_file_name, newline="") as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)
    for row in reader:
        date = row[0]
        dates.append(date)

chosen_date = st.select_slider('Selectionne une date', dates)

with open(chosen_file_name, newline="") as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)  # Ignorer la première ligne (en-tête)

    for row in reader:
        date = row[0]
        long_value = int(row[1])
        short_value = int(row[2])
        change_long_value = int(row[3])
        change_short_value = int(row[4])
        net_position_value = int(row[5])

        # Ajouter les valeurs aux tableaux correspondants
        change_long.append(change_long_value)
        change_short.append(change_short_value)
        net_position.append(net_position_value)
        
        data.append([date, change_long_value, change_short_value, net_position_value])
        if date == chosen_date:
            break

st.header(chosen_currency)
df = pd.DataFrame(data, columns=["Date", "Change long", "Change short", "Net position"])
def format_value(value):
    color = "red" if value < 0 else "green"
    return "color: %s" % color

df_styled = df.style.applymap(format_value, subset=["Change long", "Change short", "Net position"])
st.dataframe(df_styled, hide_index=True, use_container_width=True, height=3500)