from symtable import Symbol
import requests
import json
import mysql.connector
from mysql.connector import MySQLConnection
import bcrypt
from configparser import ConfigParser 
import datetime

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
    def __init__(self, name, symbol, timezone, currency, price=0):
        self.name = name
        self.symbol = symbol
        self.timezone = timezone
        self.currency = currency
        self.price = price

    @classmethod
    def search_stock(cls,keyword):
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM STOCKS WHERE company_name LIKE %s"
        cursor.execute(query, (keyword,))
        result = cursor.fetchall()
        if result is not None: 
            Stock= cls(result[0], result[1], result[2], result[3], result[4])
        else:    
            data = API_call("SYMBOL_SEARCH",keyword)
            price = API_call("GLOBAL_QUOTE",data['bestMatches'][0]['1. symbol'])
            Stock = cls(data['bestMatches'][0]['2. name'], 
                        data['bestMatches'][0]['1. symbol'], 
                        data['bestMatches'][0]['7. timezone'], 
                        data['bestMatches'][0]['8. currency'],
                        price["Global Quote"]["05. price"])
            query = "INSERT INTO STOCKS(company_name, symbol, timezone, currency, price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (Stock.name, Stock.symbol, Stock.timezone, Stock.currency, Stock.price))
            conn.commit()
            conn.close()
        return Stock