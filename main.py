import requests
import asyncio
import os
from free_sms import send_txt

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# personal info stored in env
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NUMBER = os.environ.get("PHONE_NUMBER")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# free API keys on websites
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API_KEY,
}

HOST = "smtp.gmail.com"
CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
    "bell": "txt.bell.ca"
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterdays_data = data_list[0]
yesterdays_closing_price = float(yesterdays_data["4. close"])

day_before_yesterdays_data = data_list[1]
day_before_yesterdays_closing_price = float(day_before_yesterdays_data["4. close"])

daily_difference = abs(yesterdays_closing_price - day_before_yesterdays_closing_price)
daily_percent_difference = round(daily_difference/yesterdays_closing_price*100)


if daily_percent_difference > 3:
    key_list = [key for (key,value) in data.items()]
    news_params = {
        "q" : COMPANY_NAME,
        "from" : key_list[2],
        "language":"en",
        "sortBy":"relevancy",
        "apiKey":NEWS_API_KEY
    }
    if yesterdays_closing_price - day_before_yesterdays_closing_price > 0:
        direction = "+"
    else:
        direction = "-"
    news_list = requests.get(NEWS_ENDPOINT,params=news_params)
    article_list = news_list.json()['articles'][:3]
    message = [f"{STOCK_NAME}: {direction} {daily_percent_difference}% \nHeadline: {article["title"]}. \nBrief: {article["description"]}" for article in article_list]

    for x in message:
        _num = NUMBER
        _carrier = "at&t"
        _email = EMAIL
        _pword = PASSWORD
        _msg = x
        _subj = f"{COMPANY_NAME} Update:"

        coro = send_txt(_num,_carrier,_email,_pword,_msg,_subj)
        asyncio.run(coro)

else:
    _num = NUMBER
    _carrier = "at&t"
    _email = EMAIL
    _pword = PASSWORD
    _msg = f"{STOCK_NAME} did not show significant movement today."
    _subj = f"{COMPANY_NAME} Update:"

    coro = send_txt(_num, _carrier, _email, _pword, _msg, _subj)
    asyncio.run(coro)


