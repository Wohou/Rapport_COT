import requests
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

base_url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json?id="

ids_name = ["AUD", "BRL", "BTC", "CAD", "CHF", "COPPER", "DOW JONES", "ETH", "EUR", "GAS", "GBP", "GOLD", "JPY", "MXN", "USD", "NASDAQ-100", "NZD", "OIL", "S&P 500", "SILVER", "WHEAT", "ZAR"]
ids = ["232741F","102741F","133741F","090741F","092741F","085692F","124603F","146021F","099741F","023651F","096742F","088691F","097741F","095741F","098662F","20974%2BF","112741F","067651F","13874%2BF","084691F","001602F","122741F"]

if len(ids) != len(ids_name):
    print("Error: The number of ids and names are not the same. Please verify the id and name list above.")
    exit()

pairs = list(zip(ids_name, ids))
session = requests.Session()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = PROJECT_ROOT / "csv"

def change_date(date_str):
    annee = date_str[:2]
    mois = date_str[2:4]
    jour = date_str[4:]
    return (jour + "/" + mois + "/" + annee)

def fetch_data(date_str, identifier):
    response = session.get(f"{base_url}{date_str}{identifier}")
    if response.status_code != 200:
        raise Exception("Error: API request unsuccessful.")
    data = response.json()
    if data == []:
        raise Exception("Error: API request unsuccessful. No Data found.")
    return data

# --- DATES ---
start_date_str = (datetime.now() - timedelta(days=7)).strftime("%y%m%d") # Startdate: today - 7 days (format YYMMDD)
end_date = datetime.now()   # Date de fin : Aujourd'hui
current_date = datetime.strptime(start_date_str, "%y%m%d")

total_iterations = 0

os.makedirs(CSV_DIR, exist_ok=True) # Create the folder if not exists

# Loop trough all day, day by day
while current_date <= end_date:
    date = current_date.strftime("%y%m%d")
    display_date = change_date(date)
    print(f"\n--- Test du : {display_date} ({date}) ---")

    seed_identifier = None
    seed_data = None

    # Check if at least one asset has data for this date
    for identifier in ids:
        response_test = session.get(f"{base_url}{date}{identifier}")
        if response_test.status_code == 200:
            candidate_data = response_test.json()
            if candidate_data != []:
                seed_identifier = identifier
                seed_data = candidate_data
                break

    # If date is invalid/empty, we ignore and move to the next day
    if seed_identifier is None:
        print(f"-> No data available for {display_date}.")
        current_date += timedelta(days=1)
        continue

    print("-> Data found ! Now Downloading...")
    all_data = {seed_identifier: seed_data}

    with ThreadPoolExecutor(max_workers=min(8, max(1, len(ids) - 1))) as executor:
        future_by_id = {executor.submit(fetch_data, date, identifier): identifier for identifier in ids if identifier != seed_identifier}
        for future in future_by_id:
            identifier = future_by_id[future]
            try:
                all_data[identifier] = future.result()
            except Exception as e:
                print(f"Erreur avec {identifier} à la date {date}: {e}")
                all_data[identifier] = None

    for name, identifier in pairs:
        csv_file = CSV_DIR / f"{name}.csv"

        # If the file doesn't exist we create it (with header)
        if not os.path.exists(csv_file):
            with open(csv_file, "w") as file:
                file.write("Date,Long,Short,Change Long,Change Short,Net\n")

        with open(csv_file, "r") as file:
            lines = file.readlines()

        data = all_data.get(identifier)
        if not data:
            continue

        first_item = data[0]
        key_find = [
            first_item.get("market_and_exchange_names", ""),
            first_item.get("noncomm_positions_long_all", "0"),
            first_item.get("noncomm_positions_short_all", "0"),
            first_item.get("change_in_noncomm_long_all", "0"),
            first_item.get("change_in_noncomm_short_all", "0"),
        ]

        # Net calculation: Long - Short
        long_val = int(key_find[1]) if key_find[1] else 0
        short_val = int(key_find[2]) if key_find[2] else 0
        net_val = long_val - short_val

        new_line = f"{display_date},{key_find[1]},{key_find[2]},{key_find[3]},{key_find[4]},{net_val},\n"

        # Check if the date already exists in the file (avoid duplicates)
        date_already_exists = any(line.startswith(display_date) for line in lines)

        if not date_already_exists:
            total_iterations += 1
            # Append the line just after the header (index 1)
            if len(lines) > 0:
                lines.insert(1, new_line)
            else:
                lines.append(new_line)

            with open(csv_file, "w") as file:
                file.writelines(lines)
            print(f"\t[ADD] Data appened in {name}.csv")
        else:
            pass # If the date already exists

    current_date += timedelta(days=1)

print(f"\nDone ! {total_iterations} new lines added to the CSV files.")
