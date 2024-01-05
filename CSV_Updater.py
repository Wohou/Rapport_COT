import requests

base_url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json?id="

ids_name = ["AUD", "BRL", "BTC", "CAD", "CHF", "COPPER", "DOW JONES", "ETH", "EUR", "GAS", "GBP", "GOLD", "JPY", "MXN", "USD", "NASDAQ-100", "NZD", "OIL", "S&P 500", "SILVER", "WHEAT", "ZAR"]

ids = ["232741F","102741F","133741F","090741F","092741F","085692F","124603F","146021F","099741F","023651F","096742F","088691F","097741F","095741F","098662F","20974%2BF","112741F","067651F","13874%2BF","084691F","001602F","122741F"]

# for i in range(len(ids)):
#     print(ids_name[i] + " = " + ids[i])
# Change date YY/MM/DD

date = "240102"

def change_date(date_str):
    annee = date_str[:2]
    mois = date_str[2:4]
    jour = date_str[4:]
    return (jour + "/" + mois + "/" + annee)

iteration = 0

if len(ids) != len(ids_name):
    print("Error: The number of ids and names are not the same. Please verify the id and name list above.")
    exit()

url_test = f"{base_url}{date}{ids[0]}"
response_test = requests.get(url_test)
if response_test.status_code != 200:
    print("The API request was unsuccessful.")
    exit()
if response_test.json() == []:
    print("Error: Date may be not valid.")
    exit()

for id in ids:
    name = ids_name[ids.index(id)]
    csv_file = "csv/" + name + ".csv"
    lines = []

    with open(csv_file, "r") as file:
        lines = file.readlines()

    url = f"{base_url}{date}{id}"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        raise Exception("Error: API request unsuccessful.")
    if data == []:
        raise Exception("Error: API request unsuccessful. No Data found.")
    key_to_find = ["market_and_exchange_names","noncomm_positions_long_all", "noncomm_positions_short_all", "change_in_noncomm_long_all", "change_in_noncomm_short_all"]
    key_find = []

    for item in data:
        for key in key_to_find:
            if key in item:
                key_find.append(item[key])

    print("Actually collecting data of " + name + " from " + change_date(date) + "...")
    new_line = change_date(date) + "," + key_find[1] + "," + key_find[2] + "," + key_find[3] + "," + key_find[4] + "," + str(int(key_find[1]) - int(key_find[2])) + ",\n"
    if lines[+1] != new_line:
        iteration += 1
        lines.insert(1, new_line)
    else:
        print("\tData already up to date in " + name + ".csv")

    with open(csv_file, "w") as file:
        file.writelines(lines)

print("All dones! " + str(iteration) + " files updated.")