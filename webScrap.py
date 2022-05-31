# created by: Tsz Kit Wong
# webScrap.py

from bs4 import BeautifulSoup
from os import system, name
from datetime import datetime, date, timezone
import requests
import urllib.parse
import sys


price_info = {}


def clear():
    """
    clears the console
    """
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def find_price(soup, ticker):
    results = soup.find("div", class_="D(ib) Mend(20px)")
    main_line = results.find_all("fin-streamer")

    price_info[ticker] = {}
    price_info[ticker]["curr_price"] = "$" + main_line[0].text.strip()
    price_info[ticker]["daily_change"] = main_line[1].text.strip()
    price_info[ticker]["daily_pct_change"] = main_line[2].text.strip('()')

    curr_datetime = datetime.now(timezone.utc).hour
    if curr_datetime > 20:
        after_market_results = soup.find("div", class_="Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)"). \
            find_all("fin-streamer")
        price_info[ticker]["after_market_price"] = "$" + after_market_results[1].text.strip()
        price_info[ticker]["after_market_change"] = after_market_results[2].text.strip()
        price_info[ticker]["after_market_pct_change"] = after_market_results[3].text.strip('()')


def process_link(ticker):
    link = f"https://finance.yahoo.com/quote/{ticker}/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29v" \
           f"Z2xlLmNvbS8&guce_referrer_sig=AQAAACUcyFsclu9rOyzDodJC1Cv2K0DOU0G4woBHTbUAxV0b0YnYVx35_g2_Kk" \
           f"h8C61IA4nySLZno0UVelDGvH57SGrTu5mXnkE5RbBN0xD-UxYOk-mKWiLJKR54HPtQXhL8QkOajVH3FxowIaW2lYPwJNSq" \
           f"kP9lvY7tDqeTA7ujnvu0"
    link_txt = urllib.parse.quote(link, safe="%:/?=&*+")
    # print(link_txt)
    page = requests.get(link_txt)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def refresh(soup):
    for i in price_info:
        find_price(soup, i)


def client():
    while True:
        ticker = input("Enter Stock Symbol/Ticker (ex: AMZN) - ").upper()
        clear()
        soup = process_link(ticker)
        find_price(soup, ticker)
        print(price_info)

        options_num = "1234"
        option = ""
        while True:
            choice = input(f"Enter: 1, 2, 3,or 4\n1 for continue\n2 for remove stock from list\n3 for refresh prices"
                           f"\n4 for stop\nchoice: ")
            clear()
            if choice in options_num:
                option = choice
                break
            else:
                print("Invalid Response, please try again")

        if option == "4":
            break
        elif option == "2":
            remove_stock = input("Stock to remove:  ")
            price_info.pop(remove_stock)
            print(f"New List: \n{price_info}")
        elif option == "3":
            refresh(soup)
            print(f"Prices as of {datetime.now()}: \n{price_info}")
        elif option == "continue":
            pass

    print("Program Ended")


client()
