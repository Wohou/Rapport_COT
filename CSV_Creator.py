import requests

# Add a new currency: - Catch the id on the CFTC website and give it when asked for. (XXXXXXF) (If the is a '+' in the id add '%2B' instead)
#                     - Add the id and the name to their respective list "ids" and "ids_name" in the CSV_Updater.py file
#                     - The order is important you have to put the name and the id at the same index in their respective list
#                     - Add the name in the list of currency in the comparator.py file
#
#                     - Don't forget to update the 'dates' list in this files to always have a up to date CSV file.

base_url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json?id="
id = input("Enter a ID: ") + "F"
dates = ["230703","230627","230620","230613","230606","230530","230523","230516","230509","230502","230425","230418","230411","230404","230328","230321","230314","230307","230228","230221","230214","230207","230131","230124","230117","230110","230103","221227","221220","221213","221206","221129","221122","221115","221108","221101","221025","221018","221011","221004","220927","220920","220913","220906","220830","220823","220816","220809","220802","220726","220719","220712","220705","220628","220621","220614","220607","220531","220524","220517","220510","220503","220426","220419","220412","220405","220329","220322","220315","220308","220301","220222","220215","220208","220201","220125","220118","220111","220104"
]

def change_date(date_str):
    annee = date_str[:2]
    mois = date_str[2:4]
    jour = date_str[4:]
    return (jour + "/" + mois + "/" + annee)

url_test = f"{base_url}{dates[0]}{id}"
response_test = requests.get(url_test)
if response_test.status_code != 200:
    raise Exception("Error: API request unsuccessful.")
if response_test.json() == []:
    print("Error: ID not found.")
    exit()

name = input("Enter a name for the CSV file: ")
csv_file = "csv/" + name + ".csv"
with open(csv_file, "w") as file:
    file.write("Date,Long,Short,Change long,Change short,Net position\n")
    for date in dates:
        url = f"{base_url}{date}{id}"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
                raise Exception("Error: API request unsuccessful.")
        if data == []:
            raise Exception("Error: API request unsuccessful.")
        key_to_find = ["market_and_exchange_names","noncomm_positions_long_all", "noncomm_positions_short_all", "change_in_noncomm_long_all", "change_in_noncomm_short_all"]
        key_find = []

        for item in data:
            for key in key_to_find:
                if key in item:
                    key_find.append(item[key])
        print("Actualy collecting data from the: " + change_date(date) + " to the" + change_date(dates[len(dates) - 1]))
        file.write(change_date(date) + "," + key_find[1] + "," + key_find[2] + "," + key_find[3] + "," + key_find[4] + "," + str(int(key_find[1]) - int(key_find[2])) + ",")
        file.write("\n")
