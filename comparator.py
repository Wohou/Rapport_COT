import streamlit as st
import pandas as pd
from datetime import datetime
import csv

st.header("Rapport COT")

dates = []
change_long = []
change_short = []
net_position = []
data = []

chosen_currency = st.selectbox('Selectionne un actif', ['USD', 'EUR', 'GBP', 'CHF', 'CAD', 'JPY', 'AUD', 'NZD', 'MXN', 'BRL', 'ZAR', 'BTC', 'ETH', 'OIL', 'GAS', 'GOLD', 'SILVER', 'COPPER', 'S&P 500', 'NASDAQ-100', 'DOW JONES'])
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
    next(reader)

    for row in reader:
        date = row[0]
        long_value = int(row[1])
        short_value = int(row[2])
        change_long_value = int(row[3])
        change_short_value = int(row[4])
        net_position_value = int(row[5])

        change_long.append(change_long_value)
        change_short.append(change_short_value)
        net_position.append(net_position_value)
        
        data.append([date, change_long_value, change_short_value, net_position_value])
        if date == chosen_date:
            break
    
def get_nearest_date(dates):
    today = datetime.today()
    nearest_date = None
    min_difference = float('inf')

    for date_str in dates:
        date = datetime.strptime(date_str, "%B,%d,%Y")
        difference = abs(date - today).days

        if difference < min_difference:
            min_difference = difference
            nearest_date = date

    return nearest_date

def get_next_date():
    dates = []
    today = datetime.today()
    formadted_today = today.strftime("%B-%d-%Y")
    with open("next_report.csv", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            next_date = row[0] + " " + row[1] + " " + row[2]
            dates.append(next_date)
    st.text("Date du prochain rapport: " + dates[0])

get_next_date()
st.header(chosen_currency)
df = pd.DataFrame(data, columns=["Date", "Change long", "Change short", "Net position"])
def format_value(value):
    color = "red" if value < 0 else "green"
    return "color: %s" % color

df_styled = df.style.applymap(format_value, subset=["Change long", "Change short", "Net position"])
st.dataframe(df_styled, hide_index=True, use_container_width=True, height=3500)