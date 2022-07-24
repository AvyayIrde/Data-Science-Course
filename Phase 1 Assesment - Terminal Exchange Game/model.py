from symtable import Symbol
import requests
import json
import mysql.connector
from mysql.connector import MySQLConnection
import bcrypt
from configparser import ConfigParser 
import datetime

from controller import transactions

def read_db_config(filename='data/config.ini', section='mysql'):    
        # create parser and read ini configuration file
        parser = ConfigParser()
        parser.read(filename)
        # get section, default to mysql
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section, filename))    
        return db # dictionary containing key-value pairs of the credentials to your Mysql server connection 

def API_call(function, arg):
    url = "https://alpha-vantage.p.rapidapi.com/query"
    headers = {
        "X-RapidAPI-Key": "4e11ba9a03msh6ad5ea7d0116106p196642jsn92155f1df104",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }
    if function=="SYMBOL_SEARCH":
        querystring = {
            "function":function,
            "keywords":arg,
            "datatype":"json"
        }
    elif function=="GLOBAL_QUOTE":
        querystring = {
            "function":function,
            "symbol":arg,
            "datatype":"json"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data

class account:

    def __init__(self, username, password, balance = 100000):
        self.username = username
        self.password = password
        self.balance = balance

    @classmethod
    def create_user(cls, username, password):
        user = cls(username, password)
        user.insert()

    def insert(self):
        # Insert New users into database
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO USERS(username, password, balance) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.username, self.passwordHashing(self.password), self.balance))
        conn.commit()
        conn.close()

    @staticmethod
    def passwordHashing(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')

    @classmethod
    def login(cls, username, password):
        # Login as a user
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM USERS WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result is not None:
            if bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')): #bcrypt.checkpw(password.encode('utf8'), password_hash.encode('utf8'))
                return True, cls(result[0], result[1], result[2])
            else:
                return False, None
        else:
            return False, None
    @staticmethod
    def get_users():
        # Get all users from database
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "SELECT username, balance FROM USERS"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result


class stock:
    '''
            "1. symbol": "TATACOFFEE.BSE",
            "2. name": "TATA COFFEE LTD.",
            "3. type": "Equity",
            "4. region": "India/Bombay",
            "5. marketOpen": "09:15",
            "6. marketClose": "15:30",
            "7. timezone": "UTC+5.5",
            "8. currency": "INR",
            "9. matchScore": "0.8696"
    '''
    '''
    "Global Quote": {
        "01. symbol": "TATACOFFEE.BSE",
        "02. open": "209.6500",
        "03. high": "217.8000",
        "04. low": "209.6500",
        "05. price": "217.2000",
        "06. volume": "96934",
        "07. latest trading day": "2022-07-15",
        "08. previous close": "211.4500",
        "09. change": "5.7500",
        "10. change percent": "2.7193%"
    '''
    def __init__(self, name, symbol, timezone, currency, region, price=0):
        self.name = name
        self.symbol = symbol
        self.timezone = timezone
        self.currency = currency
        self.region = region
        self.price = price

    @classmethod
    def search_stock(cls,keyword):
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        try:
            data = API_call("SYMBOL_SEARCH",keyword)
            price = API_call("GLOBAL_QUOTE",data['bestMatches'][0]['1. symbol'])
            Stock = cls(data['bestMatches'][0]['2. name'], 
                    data['bestMatches'][0]['1. symbol'], 
                    data['bestMatches'][0]['7. timezone'], 
                    data['bestMatches'][0]['8. currency'],
                    data['bestMatches'][0]['4. region'],
                    price['Global Quote']['05. price'])
        except:
            return False, None
        query = "SELECT * FROM STOCKS WHERE symbol LIKE %s"
        # cursor.execute(query, data['bestMatches'][0]['1. symbol'],)
        cursor.execute(query, (Stock.symbol,))
        result = cursor.fetchone()
        if result is not None:            
            query = "UPDATE STOCKS SET price = %s WHERE symbol = %s"
            cursor.execute(query, (float(Stock.price), Stock.symbol,))
        else:
            query = "INSERT INTO STOCKS(company_name, symbol, timezone, currency, price, region) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (Stock.name, Stock.symbol, Stock.timezone, Stock.currency, float(Stock.price), Stock.region))
        conn.commit()
        conn.close()
        return True, Stock
    
    @staticmethod
    def get_stocks():
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM STOCKS"
        cursor.execute(query,)
        result = cursor.fetchall()
        conn.close()
        return result

class trades:
    def __init__(self, user, Stock, quantity):
        self.user = user
        self.Stock = Stock
        self.quantity = quantity

    def trade_stock(self,action):
        transaction_ammount = float(self.Stock.price) * int(self.quantity)
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        if action == 'buy':
            if transaction_ammount > self.user.balance:
                return False
            else:
                query = "INSERT INTO TRADES(username, stock_symbol, price, quantity, transaction_ammount) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (self.user.username, self.Stock.symbol, float(self.Stock.price), int(self.quantity), transaction_ammount*-1.0))
                conn.commit()
                self.user.balance = self.user.balance - transaction_ammount
        elif action == 'sell':
            query = "SELECT quantity FROM TRADES WHERE username = %s AND stock_symbol = %s "
            cursor.execute(query,(self.user.username, self.Stock.symbol,))
            result = cursor.fetchall()
            owned = 0
            for i in range(0,len(result)):
                owned += result[i][0]
            if owned < self.quantity:
                return False
            else:
                query = "INSERT INTO TRADES(username, stock_symbol, price, quantity, transaction_ammount) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (self.user.username, self.Stock.symbol, float(self.Stock.price), int(self.quantity)*-1, transaction_ammount))
                conn.commit()
                self.user.balance = self.user.balance + transaction_ammount
        query = "UPDATE USERS SET balance = %s WHERE username = %s"
        cursor.execute(query, (self.user.balance, self.user.username))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def portfolio(user):
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "SELECT stock_symbol FROM TRADES WHERE username = %s"
        cursor.execute(query,(user.username,))
        result = cursor.fetchall()
        symbols = set()
        # print(result)
        for item in result:
            symbols.add(item[0])
        # print(symbols)
        portfolio = []
        for item in symbols:
            dict = {}
            query = "SELECT quantity FROM TRADES WHERE username = %s AND stock_symbol = %s"
            cursor.execute(query,(user.username,item))
            result_qty = cursor.fetchall()
            # print(resultq)
            qty=0
            for stock in result_qty:
                # print(q[0])
                qty+=stock[0]
            dict['symbol']=item
            query = 'SELECT company_name FROM STOCKS WHERE symbol = %s'
            cursor.execute(query,(dict['symbol'],))
            name = cursor.fetchone()
            dict['company_name'] = name[0]
            dict['quantity']=qty
            portfolio.append(dict)
        return portfolio

    @staticmethod
    def get_trades():
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM TRADES"
        cursor.execute(query,)
        result = cursor.fetchall()
        conn.close()
        return result
                
