import requests
import git
import os
from datetime import datetime

BASE_URL = "https://publicreporting.cftc.gov/resource/6dca-aqww.json?id="
IDS_NAME = ["AUD", "BRL", "BTC", "CAD", "CHF", "COPPER", "DOW JONES", "ETH", "EUR", "GAS", "GBP", "GOLD", "JPY",
            "MXN", "USD", "NASDAQ-100", "NZD", "OIL", "S&P 500", "SILVER", "WHEAT", "ZAR"]
IDS = ["232741F", "102741F", "133741F", "090741F", "092741F", "085692F", "124603F", "146021F", "099741F", "023651F",
       "096742F", "088691F", "097741F", "095741F", "098662F", "20974%2BF", "112741F", "067651F", "13874%2BF", "084691F",
       "001602F", "122741F"]

if len(IDS) != len(IDS_NAME):
    raise ValueError("Error: The number of ids and names are not the same. Please verify the lists.")

def change_date(date_str):
    annee, mois, jour = date_str[:2], date_str[2:4], date_str[4:]
    return f"{jour}/{mois}/{annee}"

def fetch_data(id, name, date):
    url = f"{BASE_URL}{date}{id}"
    response = requests.get(url)

    if response.status_code != 200 or not response.json():
        print(f"Error: No data found for {name}.")
        return None

    data = response.json()[0]
    key_to_find = ["market_and_exchange_names", "noncomm_positions_long_all", "noncomm_positions_short_all",
                   "change_in_noncomm_long_all", "change_in_noncomm_short_all"]

    return {key: data.get(key, "0") for key in key_to_find}

def update_csv(name, date, data):
    csv_file = f"csv/{name}.csv"

    try:
        with open(csv_file, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Warning: {csv_file} not found. Creating a new file.")
        lines = ["Date,Long,Short,Change_Long,Change_Short,Net_Position,\n"]

    new_line = f"{change_date(date)},{data['noncomm_positions_long_all']},{data['noncomm_positions_short_all']}," \
               f"{data['change_in_noncomm_long_all']},{data['change_in_noncomm_short_all']}," \
               f"{int(data['noncomm_positions_long_all']) - int(data['noncomm_positions_short_all'])},\n"

    if lines[1:] and lines[1] == new_line:
        print(f"\tData already up to date in {name}.csv")
        return False
    else:
        lines.insert(1, new_line)
        with open(csv_file, "w") as file:
            file.writelines(lines)
        return True

def update_all_data(date):
    iteration = 0
    for id, name in zip(IDS, IDS_NAME):
        print(f"Collecting data for {name} from {change_date(date)}...")
        data = fetch_data(id, name, date)
        if data and update_csv(name, date, data):
            iteration += 1
    print(f"All done! {iteration} files updated.")
    return iteration

def push_to_github():
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)

    if repo.is_dirty(untracked_files=True):
        repo.git.add("csv/")
        commit_message = f"Update data {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        repo.index.commit(commit_message)
        origin = repo.remote(name="origin")
        origin.push()
        return("Changes pushed to GitHub.")
    else:
        return("No changes detected. Nothing to push.")

def update_csv(date):
    if update_all_data(date) > 0:
        push_to_github()

if __name__ == "__main__":
    DATE = "250225"
    update_csv(DATE)
