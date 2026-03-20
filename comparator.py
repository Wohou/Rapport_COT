import streamlit as st
import pandas as pd
import csv
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Comparator COT",
    page_icon=":money_with_wings:",
    layout="wide",
)

def format_date_fr(date_value):
    mois_fr = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    return f"{date_value.day:02d} {mois_fr[date_value.month - 1]} {date_value.year}"

#------------------- Date of the next report --------------------------#
def update_next_report():
    try:
        list_day = []
        with open("next_report.csv", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                if row:
                    list_day.append(row[0])

        today = datetime.today().date()

        upcoming_report = []
        for event in list_day:
            try:
                event_date = datetime.strptime(event, '%m/%d/%y').date()
            except ValueError:
                continue
            if event_date >= today:
                upcoming_report.append(event_date)

        if upcoming_report:
            next_event = min(upcoming_report, key=lambda x: x - today)
            if next_event == today:
                return format_date_fr(next_event), True
            else:
                return format_date_fr(next_event), False

        return None, False
    except Exception:
        return None, False
#------------------------- Title ------------------------------#

st.markdown('<h3 style="text-align:center;font-weight:bold;font-size:50px;">Commitments of Traders</h3>', unsafe_allow_html=True)
# tab1, tab2, tab3 = st.tabs(["Comparateur", "Classement", "Update"])
tab1, tab2 = st.tabs(["Comparateur", "Classement"])

#------------------- Comparateur Tab --------------------------#

with tab1:
    st.markdown('<h3 style="text-align:center;font-weight:bold;font-size:40px;">⚖️ Comparateur d\'actifs financiers ⚖️</h3>', unsafe_allow_html=True)
    def Get_dates():
        dates = []
        with open("csv/USD.csv", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
                date = row[0]
                dates.append(date)
        return dates

    def get_next_date():
        data_next_report = update_next_report()
        date_formated = data_next_report[0]
        if date_formated != None:
            st.markdown(f'<h3 style="text-align:left;font-weight:bold;font-size:20px;">(📅 Date du prochain rapport : {date_formated})</h3>', unsafe_allow_html=True)
            if data_next_report[1] == True:
                st.markdown('<h3 style="text-align:left;font-size:15px;">Un nouveau rapport est disponible aujourd\'hui !</h3>', unsafe_allow_html=True)
        else:
            st.markdown('<h3 style="text-align:left;font-weight:bold;font-size:20px;">Aucune Date disponnible pour le prochain rapport</h3>', unsafe_allow_html=True)


    st.markdown('<p style="margin-top:20px"></p>', unsafe_allow_html=True)
    available_dates = Get_dates()
    chosen_date = st.select_slider('Selectionne une date', available_dates, value=available_dates[25])
    selected_entries_count = available_dates.index(chosen_date) + 1
    st.markdown(f"Nombre de jours sélectionnés : **{selected_entries_count}**")
    get_next_date()
    col1, col2 = st.columns(2)

#------ Here Update the list of currency when you add a new one, for both selectbox | Order is impoortant ---------------------------------#
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
    df_1_styled = df_1.style.map(format_value, subset=["Change long", "Change short", "Net position"])

    df_2 = pd.DataFrame(data_2, columns=["Date", "Change long", "Change short", "Net position"])
    df_2_styled = df_2.style.map(format_value, subset=["Change long", "Change short", "Net position"])

    with col1:
        st.markdown(f'<h3 style="text-align:left;font-weight:bold;font-size:30px;">{chosen_currency_1}</h3>', unsafe_allow_html=True)
        st.dataframe(df_1_styled, hide_index=True, width="stretch", height=len(df_1) * 36)

    with col2:
        st.markdown(f'<h3 style="text-align:left;font-weight:bold;font-size:30px;">{chosen_currency_2}</h3>', unsafe_allow_html=True)
        st.dataframe(df_2_styled, hide_index=True, width="stretch", height=len(df_1) * 36)


#-------------------Classement Tab--------------------------#


with tab2:
    actifs = ['USD', 'EUR', 'GBP', 'CHF', 'CAD', 'JPY', 'AUD', 'NZD', 'MXN', 'BRL', 'ZAR', 'BTC', 'ETH', 'OIL', 'GAS', 'WHEAT', 'GOLD', 'SILVER', 'COPPER', 'S&P 500', 'NASDAQ-100', 'DOW JONES']
    st.markdown('<h3 style="margin-bottom:50px;text-align:center;font-weight:bold;font-size:40px;">📊 Classement Net Position 📊</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    actif_long = []
    actif_short = []
    difference_long = []
    difference_short = []
    actif_name_long = []
    actif_name_short = []
    for actif in actifs:
        with open("csv/" + actif + ".csv", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            net_position_actuel = next(reader)[5]
            net_position_actuel_1 = next(reader)[5]
            difference = int(net_position_actuel) - int(net_position_actuel_1)
            if difference > 0:
                difference_long.append(difference)
                actif_long.append(actif)
                actif_name_long.append(actif)
            elif difference < 0:
                difference_short.append(difference)
                actif_short.append(actif)
                actif_name_short.append(actif)

    with col1:
        st.markdown('<h3 style="margin-bottom:30px;font-weight:bold;font-size:35px;">📈 Classement Position Long 📈</h3>', unsafe_allow_html=True)
        sorted_data_long = sorted(zip(actif_long, difference_long), key=lambda x: abs(x[1]), reverse=True)
        for i, (actif, difference) in enumerate(sorted_data_long):
            st.markdown(f'<p style="font-weight:bold;font-size:20px;border-radius:2%;">{i+1}. {actif}: <span style="color:#33ff33;">{difference}</span></p>', unsafe_allow_html=True)

    with col2:
        st.markdown('<h3 style="margin-bottom:30px;font-weight:bold;font-size:35px;">📉 Classement Position Short 📉</h3>', unsafe_allow_html=True)
        sorted_data_short = sorted(zip(actif_short, difference_short), key=lambda x: abs(x[1]), reverse=True)
        for i, (actif, difference) in enumerate(sorted_data_short):
            st.markdown(f'<p style="font-weight:bold;font-size:20px;border-radius:2%;">{i+1}. {actif}: <span style="color:#FF0000;">{difference}</span></p>', unsafe_allow_html=True)


