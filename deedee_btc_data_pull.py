#
#
#
#
#

#IMPORTS
# -------------------------------------------------------------------------------------------------
from imports import *
# -------------------------------------------------------------------------------------------------

#CONSTANTS
# -------------------------------------------------------------------------------------------------
FINNHUB_API_KEY = "brpqsevrh5rbpquqbvk0"
NOMICS_API_KEY = "b8bd88bf6fe905dfc2f806cf6181aea0"
API_EMAIL = "joxford88@gmail.com"
# -------------------------------------------------------------------------------------------------

# FUNCTIONS


def test():
    currency = "BTC"
    date_1 = datetime.datetime(2020, 10, 10, 1, 0, 0, 0)
    date_2 = datetime.datetime(2020, 10, 20, 1, 0, 0, 0)
    url = "https://api.nomics.com/v1/currencies/sparkline?key=" \
          + NOMICS_API_KEY \
          + "&ids=" \
          + currency \
          + "&start=" \
          + date_1.strftime("%Y-%m-%dT%H:00:00Z") \
          + "&end=" \
          + date_2.strftime("%Y-%m-%dT%H:00:00Z")
    print(urlreq.urlopen(url).read())


test()
