# import nessicary packages

from datetime import datetime
import time
import os
import ast
import json
import pandas as pd
import numpy as np
import requests as r
import time
import datetime
import pygsheets
import gspread
import df2gspread
import requests as r
from df2gspread import df2gspread as d2g


#get google sheet credentials 
scopes = ['https://www.googleapis.com/auth/spreadsheets', 
          "https://www.googleapis.com/auth/drive.file", 
          "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/sam/Documents/GitHub/PooCoin-Scraper-v1/poocoin-331423-6227f4a5365e.json', scopes)
gc = gspread.authorize(credentials)
def write_googlesheet(df,spreadsheet_key,sheet_title,starting_cell,overwrite):
    d2g.upload(df,
           spreadsheet_key,
           sheet_title,
           credentials=credentials,
           col_names=False,
           row_names=True,
           start_cell = starting_cell,
           clean=overwrite)

sheet = gc.open("Poo Coin Scraper").sheet1
numRows = len(sheet.col_values(1))

###adding custom tokens based on Jakes criteria 
sheet2 = gc.open("Poo Coin Scraper").get_worksheet(1)
custom_coin_list = sheet2.col_values(2)

CUSTOME_TOKEN_LIST = []

for i in custom_coin_list:
    CUSTOME_TOKEN_LIST.append(i)

CUSTOME_TOKEN_LIST = CUSTOME_TOKEN_LIST[1:]
 
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
    i =  eval(i)
    NESTED_DATA.append(i)

for i in NESTED_DATA:
    df = df.append(i,ignore_index=True)
    df['pancake_swap_time'] = DATE_TIME
#############GETTING CUSTOM TOKEN DATA#######################
CUSTOME_TOKEN_LIST_CALL = []
def get_data(link):
    response = r.get(link)
    json_file = response.json()
    json_file = json_file['data']
    CUSTOME_TOKEN_LIST_CALL.append(json_file)

for i in CUSTOME_TOKEN_LIST:
    i = f"https://api.pancakeswap.info/api/v2/tokens/{i}"
    get_data(i)

for i in CUSTOME_TOKEN_LIST_CALL:
    df_custom = df_custom.append(i,ignore_index=True)
    df_custom['pancake_swap_time'] = DATE_TIME

df_master = pd.concat([df,df_custom],ignore_index=True)
df_master = df_master.drop_duplicates()
print(df_master)

# write dataframe to google sheet
write_googlesheet(df_master,'1hmZ-113l1fjVrO2mhlkACWHkffsa42lKUGa31YAAw-8','Sheet1',f'A{numRows+1}',False)
print("data written")
