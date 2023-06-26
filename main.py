import requests
import config

ticker = "MSFT"

response = requests.get(f"https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/{ticker}?apikey={config.api_key}")
print(response.json())

# manipulate data here