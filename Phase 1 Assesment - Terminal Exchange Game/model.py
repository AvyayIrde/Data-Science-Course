from symtable import Symbol
import requests
import json
import mysql.connector
import bcrypt

def timezone_search():
    url = "http://api.marketstack.com/v1/timezones"
    parameters = {
        'access_key': 'afb37f15ee86604d6975ff76d5105304'
    }
    response = requests.get(url, params=parameters)
    data = json.loads(response.text)
    return data

class user:

    def __init__(self, username, password, balance = 100000):
        self.username = username
        self.password = password
        