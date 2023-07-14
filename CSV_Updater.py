# import requests

# base_url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json?id="

# ids_name = ["AUD", "BRL", "BTC", "CAD", "CHF", "COPPER", "DOW JONES", "ETH", "EUR", "GAS", "GBP", "GOLD", "JPY", "MXN", "NASDAQ-100", "NZD", "OIL", "S&P 500", "SILVER", "WHEAT", "ZAR"]

# ids = ["232741F", "102741F", "133741F", "090741F", "092741F", "146021F", "099741F", "096742F",
#     "097741F", "095741F", "112741F", "13874%2BF", "122741F", "20974%2BF", "098662F", "023651F",
#     "067651F", "084691F", "085692F", "088691F", "124603F", "001602F"
# ]
# dates = ["230703","230627","230620","230613","230606","230530","230523","230516","230509","230502","230425","230418","230411","230404","230328","230321","230314","230307","230228","230221","230214","230207","230131","230124","230117","230110","230103","221227","221220","221213","221206","221129","221122","221115","221108","221101","221025","221018","221011","221004","220927","220920","220913","220906","220830","220823","220816","220809","220802","220726","220719","220712","220705","220628","220621","220614","220607","220531","220524","220517","220510","220503","220426","220419","220412","220405","220329","220322","220315","220308","220301","220222","220215","220208","220201","220125","220118","220111","220104"
# ]

# def change_date(date_str):
#     annee = date_str[:2]
#     mois = date_str[2:4]
#     jour = date_str[4:]
#     return (jour + "/" + mois + "/" + annee)

# for id in ids:
#     for date in dates:
#         name = ids_name[ids.index(id)]
#         csv_file = "csv_date/" + name + ".csv"
#         with open(csv_file, "w") as file:
#             file.write("Date,Long,Short,Change long,Change short,Net position\n")
#             url = f"{base_url}{date}{id}"
#             response = requests.get(url)
#             data = response.json()
#             if response.status_code != 200:
#                     raise Exception("Error: API request unsuccessful.")
#             if data == []:
#                 raise Exception("Error: API request unsuccessful.")
#             key_to_find = ["market_and_exchange_names","noncomm_positions_long_all", "noncomm_positions_short_all", "change_in_noncomm_long_all", "change_in_noncomm_short_all"]
#             key_find = []

#             for item in data:
#                 for key in key_to_find:
#                     if key in item:
#                         key_find.append(item[key])
#             print("Actualy collecting data of " + name + " from the: " + change_date(date) + " to the" + change_date(dates[len(dates) - 1]))
#             file.write(change_date(date) + "," + key_find[1] + "," + key_find[2] + "," + key_find[3] + "," + key_find[4] + "," + str(int(key_find[1]) - int(key_find[2])) + ",")
#             file.write("\n")

import requests

base_url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json?id="

ids_name = ["AUD", "BRL", "BTC", "CAD", "CHF", "COPPER", "DOW JONES", "ETH", "EUR", "GAS", "GBP", "GOLD", "JPY", "MXN", "NASDAQ-100", "NZD", "OIL", "S&P 500", "SILVER", "WHEAT", "ZAR"]

ids = ["232741F", "102741F", "133741F", "090741F", "092741F", "146021F", "099741F", "096742F",
    "097741F", "095741F", "112741F", "13874%2BF", "122741F", "20974%2BF", "098662F", "023651F",
    "067651F", "084691F", "085692F", "088691F", "124603F", "001602F"
]

dates = ["230703","230627","230620","230613","230606","230530","230523","230516","230509","230502","230425","230418","230411","230404","230328","230321","230314","230307","230228","230221","230214","230207","230131","230124","230117","230110","230103","221227","221220","221213","221206","221129","221122","221115","221108","221101","221025","221018","221011","221004","220927","220920","220913","220906","220830","220823","220816","220809","220802","220726","220719","220712","220705","220628","220621","220614","220607","220531","220524","220517","220510","220503","220426","220419","220412","220405","220329","220322","220315","220308","220301","220222","220215","220208","220201","220125","220118","220111","220104"
]

def change_date(date_str):
    annee = date_str[:2]
    mois = date_str[2:4]
    jour = date_str[4:]
    return (jour + "/" + mois + "/" + annee)

for id in ids:
    name = ids_name[ids.index(id)]
    csv_file = "csv_date/" + name + ".csv"
    with open(csv_file, "a") as file:
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
                print("Actually collecting data of " + name + " from " + change_date(date) + " to " + change_date(dates[len(dates) - 1]))
                file.write(change_date(date) + "," + key_find[1] + "," + key_find[2] + "," + key_find[3] + "," + key_find[4] + "," + str(int(key_find[1]) - int(key_find[2])) + ",\n")
