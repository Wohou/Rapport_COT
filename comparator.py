import streamlit as st
import pandas as pd
import matplotlib.colors as mcolors
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
def format_value(value, column_name):
    if column_name == "net_position":
        cmap = mcolors.LinearSegmentedColormap.from_list("", ["darkred", "white", "darkgreen"])
        norm = mcolors.Normalize(vmin=-df["net_position"].max(), vmax=df["net_position"].max())
        color = mcolors.rgb2hex(cmap(norm(value)))
        return f"background-color: {color}"
    else:
        color = "red" if value < 0 else "green"
        return f"color: {color}"

df_styled = df.style.applymap(lambda x: format_value(x, "Change long"), subset=["Change long"]) \
                      .applymap(lambda x: format_value(x, "Change short"), subset=["Change short"]) \
                      .applymap(lambda x: format_value(x, "Net position"), subset=["Net position"])

st.dataframe(df_styled, hide_index=True, use_container_width=True, height=3500)