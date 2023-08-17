import requests
import config
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

ticker = "MSFT"
riskLevel = 0
# riskLevel 0, 1, or 2
api_key = os.getenv("API_KEY")

incomeStatementReq = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120&apikey={api_key}")
balanceSheetReq = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=120&apikey={api_key}")
cashFlowReq = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=120&apikey={api_key}")

if (incomeStatementReq.status_code != 200 or balanceSheetReq.status_code != 200 or cashFlowReq.status_code != 200):
    print("Failed to get data")
    exit()

# manipulate data here

incomeStatement = incomeStatementReq.json()
balanceSheet = balanceSheetReq.json()
cashFlow = cashFlowReq.json()

yearsCount = 0
avgRevenue = 0
avgGrossProfit = 0
avgOperatingMargin = 0

# 5 year average margins return
# If I have time, fit a model and then see if uptrend and downtrend and then offset avgRevenue and avgGrossProfit
for i in range(len(incomeStatement)):
    if ("revenue" in incomeStatement[i]):
        avgOperatingMargin += incomeStatement[i]["netIncome"] / incomeStatement[i]["revenue"]
        avgGrossProfit += incomeStatement[i]["grossProfit"]/(incomeStatement[i]["revenue"])
        avgRevenue += incomeStatement[i]["revenue"]
        yearsCount+=1

avgRevenue/=yearsCount
avgGrossProfit/=yearsCount
avgOperatingMargin/=yearsCount

print(avgRevenue)
print(avgGrossProfit)
print(avgOperatingMargin)
print("---------------------------")

estimatedEBIT = avgRevenue*avgOperatingMargin
estimatedEBIT *= (1-config.avgRateOfTax)
estimatedEBITDA = cashFlow[0]["depreciationAndAmortization"] + estimatedEBIT
estimatedEBITDA*=(1-config.retainedForGrowth)

print(estimatedEBIT)
print(estimatedEBITDA)

# Calculate Earning Power Value

EPV = estimatedEBITDA / (config.costOfDebt[riskLevel]*config.debtFinancingRatio+config.costOfEquity[riskLevel]*(1-config.debtFinancingRatio))
print(EPV)