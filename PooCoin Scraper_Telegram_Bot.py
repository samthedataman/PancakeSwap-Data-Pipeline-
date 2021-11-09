# import nessicary packages
# bro its "neccessary"
import os
from telebot import TeleBot
from dotenv import load_dotenv
import selenium 
from selenium import webdriver
import pandas as pd
import numpy as np
import requests as r
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
import datetime
import pygsheets
import gspread
import df2gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

# load_dotenv()
# BOT_KEY = '2132930219:AAGTBcCo9-pwFWLkB_0XfuH9U0A56zOEqXY'
scopes = ['https://www.googleapis.com/auth/spreadsheets', 
          "https://www.googleapis.com/auth/drive.file", 
          "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/sam/Desktop/PooCoin Scraper/poocoin-331423-6227f4a5365e.json', scopes)
gc = gspread.authorize(credentials)
def write_googlesheet(df,spreadsheet_key,sheet_title,starting_cell,overwrite):
    d2g.upload(df,
           spreadsheet_key,
           sheet_title,
           credentials=credentials,
           col_names=True,
           row_names=True,
           start_cell = starting_cell,
           clean=overwrite)

def clean_price(col):
    re.sub(r['A-Za-Z'],'',col)

#create empy attribute list of desirable scraping elements off of grailed.com
market_cap_list = []
name_list = []
total_supply_list = []
current_price_list = []
date_list = []
#open chrome driver on your machine
driver = webdriver.Chrome('/Users/sam/Downloads/chromedriver-2')
#open poo coin
COIN_LINKS = [
    'https://poocoin.app/tokens/0xd74b782e05aa25c50e7330af541d46e18f36661c',
'https://poocoin.app/tokens/0x2a9718deff471f3bb91fa0eceab14154f150a385',
'https://poocoin.app/tokens/0x33a3d962955a3862c8093d1273344719f03ca17c',
'https://poocoin.app/tokens/0xc001bbe2b87079294c63ece98bdd0a88d761434e',
'https://poocoin.app/tokens/0xda6802bbec06ab447a68294a63de47ed4506acaa',
'https://poocoin.app/tokens/0x79ebc9a2ce02277a4b5b3a768b1c0a4ed75bd936',
'https://poocoin.app/tokens/0x72d2946094e6e57c2fade4964777a9af2b7a51f9',
'https://poocoin.app/tokens/0xc3262500039696ff8ef9830fb422ab32b15bd366']
index = 0
for coin in COIN_LINKS[0:1]:
    driver.get(coin)
    time.sleep(10)
    #scrape name 
    name = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1").get_attribute("textContent")
    name_list.append(name)
    print(name)
    #scrape marketcap
    market_cap = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div[1]/div[2]/span[2]").get_attribute("textContent")
    market_cap_list.append(market_cap)
    print(market_cap)
    #Size of Liquidity Pool v1 or v2 (if available)
    #Token Address
    #scrape supply
    total_supply = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div[1]/div[2]").get_attribute("textContent")[0:50]
    total_supply = [i for i in total_supply if i.isdigit()]
    total_supply  = ''.join(map(str,total_supply))
    total_supply = int(total_supply)
    total_supply_list.append(total_supply)
    print(total_supply)
    #scrape current price
    current_price = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div").get_attribute("textContent")
    current_price_list.append(current_price)
    print(current_price)
    #scrape date
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_list.append(date)
    time.sleep(10)
    index +=1
    print(f'scraping {index} page')

poo_dictionary = dict(zip(["Coin Ticker",
"Market Cap",
"Total Supply",
"Current Price",
"Time of Scrape"],
[name_list,market_cap_list,total_supply_list,current_price_list,date_list]))

#turn dictionary into a dataframe and transpose to show tabular format
Poocoin_dataframe = pd.DataFrame.from_dict(poo_dictionary ,orient='index').transpose()
Poocoin_dataframe['Current Price'].str.replace(r[''])
print(Poocoin_dataframe)
write_googlesheet(Poocoin_dataframe,'1hmZ-113l1fjVrO2mhlkACWHkffsa42lKUGa31YAAw-8','Sheet1','A1',False)
print("data written")
# bot = TeleBot(__name__)


# @bot.route('/coins')
# def weather(message, cmd):
#     chat_dest = message['chat']['id']
#     bot.send_message(chat_dest, poo_dictionary)


# if __name__ == '__main__':
#     bot.config['api_key'] = BOT_KEY
#     bot.poll(debug=True)