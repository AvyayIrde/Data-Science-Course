#stdio mask to mask passwords from user view
import stdiomask

def menu():
    menu='''
    Welcome to the banker app
    1. Create account
    2. Login
    3. Exit\n'''
    choice = input(menu)
    return choice

def create_acc():
    username = input('Hi user, Enter your username to create account: ')
    attempts = 0
    while(attempts != 5):
        pass_in_1 = stdiomask.getpass(prompt='Enter your password\t: ')
        pass_in_2 = stdiomask.getpass(prompt='Re-Enter your password\t: ')
        if pass_in_1 == pass_in_2:
            print('Passwords match')
            password =  pass_in_1
            return username, password
        else:
            print('Passwords dont match. Retry')
            attempts += 1
    print("too many failed attempts!!")


def success_acc():
    print('Account has been successfully created and you are logged in')

def trans_options():
    menu = '''
    1. Check Balance
    2. Deposite
    3. Withdraw
    4. Log out\n'''
    choice = input(menu)
    return choice

def diplay_balance(acc):
    print(f"Hello {acc.username} Your current bank balance is {acc.balance}")
    return

def get_deposit():
    deposit = float(input('Hello, enter the ammount you wish to deposit: '))
    return deposit

def get_withdraw():
    withdraw = float(input('Hello, enter the ammount you wish to deposit: '))
    return withdraw

def incorrect_choice():
    print("Invalid choice, retry!")
    return

def login():
    acc_no = input("Enter your acc_no")
    password = stdiomask.getpass(prompt='Enter your password')
    return acc_no,password

def invalid_creds():
    print("The entered Account number doesn't exist or the password was incorrect")

def success_login():
    print("Login Successful!!")

def exit():
    print("Thank you for using our banker app")