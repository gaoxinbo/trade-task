
from urllib.request import urlopen
from urllib.parse import urlencode
import json

APIKey = 'VSC53P9QMT9DCHHL'
EndPoint = 'https://www.alphavantage.co/query'

def query(func, symbol):
  url = "{}?function={}&symbol={}&apikey={}".format(EndPoint, func, symbol, APIKey)
  response = urlopen(url) 
  return response.read().decode('utf-8')

     


def queryDaily(symbol):
  return parse(json.loads(query('TIME_SERIES_DAILY', symbol)))


def parse(data):
  l = []
  d = data['Time Series (Daily)']
  for key,value in d.items():
    record = {}
    record['date'] = key[0:10]
    record['close'] = value['4. close']
    record['open'] = value['1. open']
    record['high'] = value['2. high']
    record['low'] = value['3. low']
    record['volume'] = value['5. volume']

    l.append(record)

  return l

if __name__ == '__main__':
  print(queryDaily('FB'))
