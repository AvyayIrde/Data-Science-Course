import stdiomask

def onboard():
    menu = '''
    Welcome to the terminal Exchange game
    1. Create Account
    2. Login
    3. Exit
    '''
    choice = input(menu)
    return choice

def create_account():
    username = input('Hi user, Enter your username to create account\t: ')
    attempts = 0
    while(attempts != 5):
        pass_in_1 = stdiomask.getpass(prompt='Enter your password\t\t: ')
        pass_in_2 = stdiomask.getpass(prompt='Re-Enter your password\t\t: ')
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
    if username is not None:
        print('Login successful!\nWelcome {}'.format(username))
    else:
        print('Operation successful!')

def operation_failed(username=None):
    if username is not None:
        print('Username: "{}" alerady Exists\nTry again!'.format(username))
    else:
        print('Operation failed!\nTry again using different username and password')

def login():
    username = input('Enter your username\t: ')
    password = stdiomask.getpass(prompt='Enter your password\t: ')
    return username, password

def exit():
    print("Thank you for playing!")