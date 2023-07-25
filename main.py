import requests
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

parameters_stock = {

    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.environ.get("Key")

}

account_sid = os.environ.get("Acc-Sid")
auth_token = os.environ.get("Auth-Token")

response = requests.get(url="https://www.alphavantage.co/query", params=parameters_stock)
response.raise_for_status()

data = response.json()

stock_data = data["Time Series (Daily)"]
date_list = list(data["Time Series (Daily)"])
yesterday = date_list[0]
bef_yesterday = date_list[1]

close = "4. close"

parameters_news = {
    "q": COMPANY_NAME,
    "from": date_list[0],
    "sortBy": "popularity",
    "apiKey": "fc4159db43774750b0e0798adfc5b8b3"

}


difference = float(stock_data[yesterday][close]) - float(stock_data[bef_yesterday][close])
percentage = round(100 * (abs(difference) / float(stock_data[bef_yesterday][close])))

if difference < 0:
    fluctuation = "🔻"
else:
    fluctuation = "🔺"


if percentage >= 5:

    response = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    response.raise_for_status()
    data = response.json()

    for i in range(3):

        try:
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                 body=f'{STOCK}: {fluctuation}{percentage}% \nHeadline: {data["articles"][i]["title"]} \n'
                      f'Brief: {data["articles"][i]["description"]}',
                 from_= os.environ.get("from-Phone"),
                 to= os.environ.get("to-Phone")
                )
        except IndexError:
            break

