from locale import currency
import stdiomask
import pandas as pd
from tabulate import tabulate
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def onboard():
    menu = '''
    Welcome to the terminal Exchange game
    1. Create Account
    2. Login
    3. Exit
    4. Or type secert code to enter admin menu
    '''
    choice = input(menu)
    return choice

def create_account():
    print("Welcome new user")
    username = input('Enter a username to create account\t: ')
    attempts = 0
    while(attempts != 5):
        pass_in_1 = stdiomask.getpass(prompt='Enter a password for the account\t: ')
        pass_in_2 = stdiomask.getpass(prompt='Re-Enter the password\t\t\t: ')
        if pass_in_1 == pass_in_2:
            print('Passwords match')
            password =  pass_in_1
            return True, username, password
        else:
            print('Passwords dont match. Retry')
            attempts += 1
    print("too many failed attempts!!")
    return False, None, None

def operation_successsfull(username=None):
    clear()
    if username is not None:
        print('Login successful!\nWelcome {}'.format(username))
    else:
        print('Operation successful!')

def operation_failed(username=None):
    clear()
    if username is not None:
        print('Username: "{}" alerady Exists\nTry again!'.format(username))
    else:
        print('Operation failed!')

def login():
    username = input('Enter your username\t: ')
    password = stdiomask.getpass(prompt='Enter your password\t: ')
    return username, password

def exit():
    print("Thank you for playing!")

def transactions_menu():
    menu = '''
    1. Search Stock
    2. Buy stock
    3. Sell stock
    4. View portfolio
    5. Logout
    '''
    choice = input(menu)
    return choice 

def search_stock():
    keyword = input("Enter name of company\t: ")
    return keyword


def stock_info(Stock):
    print('''
    Company Name\t: {}
    Symbol\t\t: {}
    Timezone\t\t: {}
    Region\t\t: {}
    Currency\t\t: {}
    Price\t\t: {}
    '''.format(Stock.name, Stock.symbol, Stock.timezone, Stock.region, Stock.currency, Stock.price))

def trade_stock():
    symbol = input("Enter symbol of the stock you want to trade in\t: ")
    return symbol

def stock_quantity(Stock, user):
    print('''
    Avaiable Balance\t: {}
    Stock Name\t\t: {}
    Stock Symbol\t: {}
    Stock Price\t\t: {}
    Stock Currency\t: {} 
    '''.format(user.balance, Stock.name, Stock.symbol, Stock.price, Stock.currency))
    quantity = int(input("Enter the amount of stock you want to trade : ")) 
    return quantity

def view_portfolio(user, portfolio):
    print('''
    Username\t: {}
    Avaiable Balance\t: {}
    Profit/Loss\t: {}
    Stocks in Portfolio\t:
    '''.format(user.username,user.balance,int(user.balance-100000)))
    for item in portfolio:
        print('''
        Company Name\t: {}
        Stock symbol\t: {}
        Quantity Owned\t: {}
        '''.format(item['company_name'], item['symbol'], item['quantity']))

def admin_menu():
    menu = '''
    1. View all users
    2. View all stocks in database
    3. View all trades
    4. Logout
    '''
    choice = input(menu)
    return choice



def view_users(users):
    df = pd.DataFrame(users)
    df.columns=['Username', 'Balance']
    print(tabulate(df, headers='keys', tablefmt='pretty', stralign='left'))

def view_stocks(stocks):
    df = pd.DataFrame(stocks)
    df.columns=['Company Name', 'Symbol', 'Timezone', 'Currency', 'Price', 'Region']
    print(tabulate(df, headers='keys', tablefmt='pretty', stralign='left'))
    
def view_trades(trades):
    df = pd.DataFrame(trades)
    df.columns=['Index', 'Username', 'Company Symbol', 'Price', 'Quantity', 'Transaction Ammount', 'TimeStamp']
    print(tabulate(df, headers='keys', tablefmt='pretty', stralign='left', showindex=False))