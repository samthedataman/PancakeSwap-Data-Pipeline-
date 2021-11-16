# PooCoin Scraper

This program is a python request cyrptocurrency price engine hosted on an AWS EC2 cloud instance.

Its purpose is to update a google sheet every minute with live pricing data of the top 1000 bnb pairs leveraging the Pancakeswap API. In addition to the top 1000 pairs the program also can take new token addresses dynamically by user input into the google sheet make the the program modular for future coin releases.

Future updates to this program will include the addition of more API's such as the BSC scan API to allow for dyamic address P/l updates and token holdings by holder. As well as coin market caps and total supply KPI's to be added in the near future.

Please note that the raw data coming from the uniswap api is not clean and data massaging was used to clean the raw data to present attrubutes such as token address by token.


