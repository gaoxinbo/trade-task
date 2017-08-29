#!/usr/bin/env python

import sys
import logging

import config

import yahoo_finance 
import pymysql

import api

def print_err_and_exit():
    print("Usage: password")
    sys.exit(-1)

def get_logger():
    logger = logging.getLogger("daily_fetch")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)


    logger.addHandler(ch)

    return logger

 

def get_connection(passwd):
    connection = pymysql.connect(host=config.RDS_ENDPOINT,
                                 user=config.USERNAME,
                                 db=config.DB,
                                 password=passwd)
    return connection

def download_data_v2(conn, symbol):
    logger.info("fetching " + symbol)
    data = api.queryDaily(symbol)
    for item in data:
      opt = [] 
      opt.append(symbol)
      opt.append(item['date'])
      opt.append(item['open'])
      opt.append(item['close'])

      with conn.cursor() as cursor:
          query = "select * from daily_price where symbol = %s and trade_date = %s"
          l = []
          l.append(symbol)
          l.append(opt[1])

          cursor.execute(query, l)
          result = cursor.fetchone()
          if result:
              logger.info("skip %s %s" % (l[0], l[1]))
              continue 

      with conn.cursor() as cursor:
          sql = "replace into daily_price (symbol, trade_date, open_price, close_price) values (%s, %s, %s, %s)"
          cursor.execute(sql, opt)
          logger.info(opt)
          conn.commit()

    return
 

def download_data(conn, symbol):
    logger.info("fetching " + symbol)
    s = yahoo_finance.Share(symbol)
    opt = [] 
    opt.append(symbol)
    opt.append(s.get_trade_datetime()[0:10])
    opt.append(s.get_open())
    opt.append(s.get_price())

    with conn.cursor() as cursor:
        query = "select * from daily_price where symbol = %s and trade_date = %s"
        l = []
        l.append(symbol)
        l.append(opt[1])

        cursor.execute(query, l)
        result = cursor.fetchone()
        if result:
            logger.info("skip %s %s" % (l[0], l[1]))
            return

    with conn.cursor() as cursor:
        sql = "replace into daily_price (symbol, trade_date, open_price, close_price) values (%s, %s, %s, %s)"
        cursor.execute(sql, opt)
        logger.info(opt)
        conn.commit()

    return
  
if __name__ == '__main__':
    if len(sys.argv) <  2:      
        print_err_and_exit()
      

    logger = get_logger()
    logger.info("start...")
    conn = get_connection(sys.argv[1])


    for symbol in config.SYMBOL_LIST:
        try:
            download_data_v2(conn, symbol)
        except Exception as err:
            logger.info(err)
            continue

    logger.info("end")
