from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from PyQt6 import QtCore, QtGui, QtWidgets
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'start':'1',
  'limit':'5000',
  'symbol':'BTC'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '8bc7959e-153c-40dd-8da9-34e544661e71',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)