# import nessicary packages
from datetime import datetime
import time
import os
import ast
import json
import pandas as pd
import numpy as np
import requests as r
import regex as re
import time
import datetime
import pygsheets
import gspread
import df2gspread
import requests as r
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

#get google sheet credentials 
scopes = ['https://www.googleapis.com/auth/spreadsheets', 
          "https://www.googleapis.com/auth/drive.file", 
          "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('PooCoin-Scraper-v1/poocoin-331423-6227f4a5365e.json', scopes)
gc = gspread.authorize(credentials)

#opening google sheet Poo Coin Scraper v2
sheet = gc.open("Poo Coin Scraper v2")
           
# getting sheet dimension for Poocoin Live Data Feed

Poocoin_Live_Data_Feed = sheet.worksheet("Poocoin Live Data Feed")

#####get live price data from 1000 coin pairs every 6 minutes #####
df = pd.DataFrame()
df_custom = pd.DataFrame()
#getting top 1000 bnb pairs from sushiswap api
request = r.get("https://api.pancakeswap.info/api/v2/tokens")
data = request.json()
UNIX_TIME = data['updated_at']
DATE_TIME = datetime.datetime.fromtimestamp(UNIX_TIME / 1e3)
TOKEN_ADDRESSES = []
for i in data['data']:
    TOKEN_ADDRESSES.append(i)

TOKEN_DATA = []

for i in TOKEN_ADDRESSES:
    token = f"data['data']['{i}']"
    TOKEN_DATA.append(token)

NESTED_DATA =[]

for i in TOKEN_DATA:
    j =  eval(i)
    j['token_address'] = i
    NESTED_DATA.append(j)

for i in NESTED_DATA:
    df = df.append(i,ignore_index=True)
df['pancake_swap_time'] = DATE_TIME
df['pancake_swap_time'] =df['pancake_swap_time'].astype('string')
df['token_address'] = df['token_address'].astype('string')
df['token_address'] = df['token_address'].apply(lambda x: x.replace("'",""))
df['token_address'] = df['token_address'].apply(lambda x: x.replace("']",""))
df['token_address'] = df['token_address'].apply(lambda x: x.replace("data[data][",""))
df['token_address'] = df['token_address'].apply(lambda x: x.replace("]",""))
df['price'] = df['price'].astype('float')
df['price_BNB'] = df['price_BNB'].astype('float')
print('done with standard api calls')
# ###adding custom tokens based on Jakes criteria 
Poocoin_Custom_Tokens = sheet.worksheet("Custom Token List")
custom_coin_list_sheet = Poocoin_Custom_Tokens.col_values(2)
CUSTOME_TOKEN_LIST = []

for i in custom_coin_list_sheet:
    CUSTOME_TOKEN_LIST.append(i)

CUSTOME_TOKEN_LIST = CUSTOME_TOKEN_LIST[1:]
CUSTOME_TOKEN_LIST_APPEND = []
index = 0
for i in CUSTOME_TOKEN_LIST:
    link = f"https://api.pancakeswap.info/api/v2/tokens/{i}"
    response = r.get(link)
    json_file = response.json()
    json_file = json_file['data']
    json_file['token_address'] = i
    CUSTOME_TOKEN_LIST_APPEND.append(json_file)
    df_custom = df_custom.append(CUSTOME_TOKEN_LIST_APPEND,ignore_index=True)
    index +=1
    print(f'{index/len(CUSTOME_TOKEN_LIST)}% of custom tokens downloaded')

df_custom['pancake_swap_time'] = DATE_TIME
df_custom['pancake_swap_time'] = df_custom['pancake_swap_time'].astype('string')
df_custom['price'] = df_custom['price'].astype('float')
df_custom['price_BNB'] = df_custom['price_BNB'].astype('float')


df_master = pd.concat([df,df_custom],ignore_index=True)
df_master = df_master.drop_duplicates()
print(df_master)



gc = gspread.authorize(credentials)
spreadsheet_key = '1y0On2rQOxf1G-213MMCb10ywGShFKTSufP-HAm2ZysA'
wks = 'Poocoin Live Data Feed'
spreadsheet = gc.open_by_key(spreadsheet_key)
values = [df_master.columns.values.tolist()]
values.extend(df_master.values.tolist())
spreadsheet.values_update(wks, params={'valueInputOption': 'USER_ENTERED'}, body={'values': values})
print("data loaded to sheet")

