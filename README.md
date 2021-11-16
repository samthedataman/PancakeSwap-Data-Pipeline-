# PooCoin Scraper

This program is a dynamic python request cyrptocurrency price engine hosted on an AWS EC2 cloud instance updating every ~ 1 minute.

Its purpose is to provide users with an aggregate, live pricing data for the top 1000 bnb pairs leveraging the Pancakeswap API.

In addition to the top 1000 pairs the program also can ingest new token addresses dynamically by user input into the google sheet making the the program modular for future coin releases.

KPI's Retrieved :

Name (Name of Token)
Symbol (Symbol of Token)
Price (Price of token in $USD)
Price_BNB (Price of token denotated in BNB)
Token_address (Address of Specific Token)
Pancake_swap_time (time of request)

Future updates to this program will include the addition of more API's such as the BSC scan API to allow for dyamic address P/l updates and token holdings by holder. As well as coin market caps and total supply KPI's to be added in the near future.

Please note that the raw data coming from the uniswap api is not clean and data massaging was used to clean the raw data to present attrubutes such as token address by token.

API's in use : https://github.com/pancakeswap/pancake-info-api/blob/develop/v2-documentation.md

Enpoints used : 

Tokens :https://api.pancakeswap.info/api/v2/tokens 
Specific Tokens :https://api.pancakeswap.info/api/v2/tokens/0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82





