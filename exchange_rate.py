import os

EXCHANGE_RATES = {}

def load_exchange_rates():
  directory = "hmrc_exchange_rate/"
  for filename in os.listdir(directory):
    if filename.endswith(".csv"):
      file_path = os.path.join(directory, filename)
      with open(file_path, "r") as file:
        for line in file:
          values = line.strip().split(",")
          currency = values[2]
          rate = values[3]
          if currency != "USD":
            continue
          month_and_year = filename.split("-")[2].split(".")[0]
          EXCHANGE_RATES[month_and_year] = float(rate)


def get_exchange_rate(date):
  month = date.split('/')[1]
  year = date.split('/')[2]

  return EXCHANGE_RATES.get(f"{month}{year}", 1.0)
