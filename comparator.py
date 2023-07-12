import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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

def jours_entre_dates(date1, date2):
    difference = date2 - date1
    

# def Get_next_date():
#     file_path = "next_report.csv"
#     dates = []
#     with open(file_path, "r") as file:
#         csv_reader = csv.reader(file)
#         for row in csv_reader:
#             mois, jour, annee = row[0], row[1], row[2]
#             date_str = f"{mois} {jour} {annee}"
#             date = datetime.strptime(date_str, "%B %d %Y")
#             dates.append(date)

#     aujourd_hui = datetime.today()
#     date_plus_proche = min(dates, key=lambda date: abs(date - aujourd_hui))
#     nb_jours = (date_plus_proche - aujourd_hui).days + 1
#     date_formatee = date_plus_proche.strftime("%d %B %Y")
#     st.text("Le prochain rapport COT sortira le " + date_formatee + " il reste alors " + str(nb_jours) + " jours.")

# Get_next_date()
st.header(chosen_currency)
df = pd.DataFrame(data, columns=["Date", "Change long", "Change short", "Net position"])
def format_value(value):
    color = "red" if value < 0 else "green"
    return "color: %s" % color

df_styled = df.style.applymap(format_value, subset=["Change long", "Change short", "Net position"])
st.dataframe(df_styled, hide_index=True, use_container_width=True, height=3500)