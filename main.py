import requests
import config

ticker = "MSFT"

incomeStatementReq = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement-as-reported/{ticker}?limit=10&apikey={config.api_key}")

incomeStatement = incomeStatementReq.json()

# manipulate data here

if (incomeStatementReq.status_code != 200):
    print("Failed to get Income Statements")
    exit()



yearsCount = 0
avgRevenue = 0
avgGrossProfit = 0

# 5 year average margins return
# If I have time, fit a model and then see if uptrend and downtrend and then offset avgRevenue and avgGrossProfit
for i in range(5):
    if ("revenuefromcontractwithcustomerexcludingassessedtax" in incomeStatement[i]):
        grossProfit = incomeStatement[i]["revenuefromcontractwithcustomerexcludingassessedtax"] - incomeStatement[i]["costofgoodsandservicessold"]
        avgRevenue += (incomeStatement[i]["revenuefromcontractwithcustomerexcludingassessedtax"])
        avgGrossProfit += grossProfit/(incomeStatement[i]["revenuefromcontractwithcustomerexcludingassessedtax"])
        yearsCount+=1

avgRevenue/=yearsCount
avgGrossProfit/=yearsCount

print(avgRevenue)
print(avgGrossProfit)
print("---------------------------")

estimatedEBIT = avgRevenue*avgGrossProfit
