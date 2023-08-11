import requests
import smtplib

## STOCK API: https://www.alphavantage.co/documentation/#daily
# NEWS API: https://newsapi.org/

stock = input("Enter Stock Name: ")
company = input("Enter Company Name: ")

STOCK_NAME = f"{stock}"                       #e.g. TSLA
COMPANY_NAME = f"{company}"                   #e.g.Tesla Inc

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "API KEY"
NEWS_API_KEY = "API KEY"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]

#TODO 1. - Get yesterday's closing stock price.
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_data = yesterday_data["4. close"]
print(yesterday_closing_data)

#TODO 2. - Get the day before yesterday's closing stock price
yesterday_data = data_list[1]
daybeforeyesterday_closing_data = yesterday_data["4. close"]
print(daybeforeyesterday_closing_data)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
difference_in_closing = abs(float(yesterday_closing_data) - float(daybeforeyesterday_closing_data))
print(difference_in_closing)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = ((difference_in_closing)/float(yesterday_closing_data)) * 100
print(percentage_difference)

#TODO 5. - If TODO4 percentage is greater than 5 then send an email to the user regarding their 'STOCK_NAME' AND 'COMPANY_NAME'.
if percentage_difference > 5:
#TODO 6. - Use the News API to get articles related to the COMPANY_NAME.

    news_parameters = {
        "qIntitle": COMPANY_NAME,
        "apikey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    article = news_response.json()["articles"]

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = article[:3]

#TODO 8. - Create a new list of the first 3 article's headline and description.
    formatted_article = [f"Headline: {article['title']}. \nBrief:{article['description']}" for article in three_articles]
    print(formatted_article)
#TODO 9. - Send each article as a separate mail.

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    formatted_article = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    all_articles = "\n\n".join(formatted_article)

    my_email = "MAIL_ID"
    password = "PASSWORD"
    recipient_email = "RECIPIENT MAIL"

    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = recipient_email
    msg["Subject"] = "Stock Closing Update"

    msg.attach(MIMEText(all_articles, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=recipient_email, msg=msg.as_string())
