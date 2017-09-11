
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
    if len(key) != 10:
      continue
    record = {}
    record['date'] = key[0:10]
    record['close'] = str(round(float(value['4. close']),2))
    record['open'] = str(round(float(value['1. open']),2))
    record['high'] = str(round(float(value['2. high']),2))
    record['low'] = str(round(float(value['3. low']),2))
    record['volume'] = value['5. volume']

    l.append(record)

  return l

if __name__ == '__main__':
  print(queryDaily('FB'))
