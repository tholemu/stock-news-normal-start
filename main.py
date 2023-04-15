import requests
import smtplib
import html

MY_EMAIL = "bowlermj84@gmail.com"
MY_PASSWORD = "esxozymdjxlwazno"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "E0B04JUL2447QI59"
NEWS_API_KEY = "160ee43b7d8f46349d2b0242d53c5970"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

news_params = {
    "apikey": NEWS_API_KEY,
    "qinTitle": COMPANY_NAME,
    "language": "en",
}

 ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = (yesterday_data["4. close"])
print(f"The price of {STOCK_NAME} closed at a price of {yesterday_closing_price} yesterday")

#TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = (day_before_yesterday_data["4. close"])
print(f"The price of {STOCK_NAME} closed at a price of {day_before_yesterday_closing_price} the day before yesterday")

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(f"The positive difference between yesterday's and the day before yesterday's {STOCK_NAME} price was {difference}")

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_difference = (difference / float(yesterday_closing_price)) * 100
print(f"The percentage difference between yesterday's and the day before yesterday for {STOCK_NAME} is {percentage_difference}")

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

# if percentage_difference > 5:
#     print("Get News")



    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

if percentage_difference > 0:
    # print("Get News")
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    three_articles = news_data[:3]
    print(three_articles)


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

    for article in three_articles:
        # formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
        article['description'] = article['description'].replace('“', '"')
        article['description'] = article['description'].replace('“', '"')
        article['description'] = article['description'].replace('”', '"')
        article['description'] = article['description'].replace('…', '...')
        formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}"]
    formatted_articles = formatted_articles
    print(formatted_articles)
    
#TODO 9. - Send each article as a separate message via Twilio.
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Tesla News\n\n {formatted_articles}"
        )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

