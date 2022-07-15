from symtable import Symbol
import requests
import json
import mysql.connector
from mysql.connector import MySQLConnection
import bcrypt
from configparser import ConfigParser 

# def timezone_search():
#     url = "http://api.marketstack.com/v1/timezones"
#     parameters = {
#         'access_key': 'afb37f15ee86604d6975ff76d5105304'
#     }
#     response = requests.get(url, params=parameters)
#     data = json.loads(response.text)
#     return data

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