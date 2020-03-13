import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.de/Strength-Creative-Decorative-Lighting-Children/dp/B07RTLKY7K/ref=sr_1_10?__mk_de_DE=ÅMÅŽÕÑ&keywords=dragon+ball+z&qid=1584127458&sr=8-10'
# Information about browser
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
}


def check_price():
    # Pulls all the data from the website
    page = requests.get(URL, headers=headers)

    # Pull out individual pieces from the website
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id='productTitle').get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[0:5].replace(',', '.'))

    if converted_price < 20.00:
        send_mail()

    print(converted_price)
    print(title.strip())


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    # Encrypts connection
    server.starttls()
    server.ehlo()

    server.login('senderemail@somethin.com', 'password')

    subject = "Price fell down"
    body = "Check the Amazon link https://www.amazon.de/Strength-Creative-Decorative-Lighting-Children/dp/B07RTLKY7K/ref=sr_1_10?__mk_de_DE=ÅMÅŽÕÑ&keywords=dragon+ball+z&qid=1584127458&sr=8-10"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'senderemail@somethin.com',
        'recieveremail@something.com',
        msg.encode('utf8')
    )
    print("Email has been sent!!")

    server.quit()

# Check for price drop every day
while True:
    check_price()
    time.sleep(86400)

