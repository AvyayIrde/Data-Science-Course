# build a MVC bacnk application
# 1. Enable user to create account
# 2. Enable user to login
# 3. Persist the data in a JSON file
# 4. Enable user to deposit/wthdraw money and update the bank balance
# 5. Add appropriate error handling messages 

import model as m
import view as v

def onboard():
    '''
    Welcome to the banker app
    1. Create account
    2. Login
    3. Exit'''
    choice = None
    while (choice != '3'):
        choice = v.menu()
        if choice == '1':
            username,password = v.create_acc()
            status,acc = m.account.create_acc(username, password)
            v.success_acc()
            onboard()
        elif choice == '2':
            username,password=v.login()
            status,acc = m.account.login(username,password)
            while status == False:
                v.invalid_creds()
                username,password=v.login()
                status,acc = m.account.login(username,password)
            v.success_login()
            transactions(acc)
        elif choice =='3':
            v.exit()
            exit()
        else:
            v.incorrect_choice()
            onboard()

def transactions(acc):
    '''
    1. Check Balance
    2. Deposit
    3. Withdraw
    4. Log out'''
    choice = None
    while (choice != '4'):
        choice = v.trans_options()
        if choice == '1':
            v.diplay_balance(acc)
        elif choice == '2':
            deposit = v.get_deposit()
            status = acc.deposit_money(deposit)
        elif choice == '3':
            withdraw = v.get_withdraw()
            status = acc.withdraw_money(withdraw)
        elif choice == '4':
            return
        else:
            v.incorrect_choice()
            transactions(acc)
            
if __name__ =='__main__':
    onboard()