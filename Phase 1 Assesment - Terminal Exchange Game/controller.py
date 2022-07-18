import model as m
import view as v
import mysql.connector.errors

# Onbard:
# Create Account 
# login
# Exit

#Transctions:
# Search stock
# Buy stock
# Sell stock
# View portfolio
# Check balance


def onboard():
    '''
    1. Create Account
    2. Login
    3. Exit
    '''
    choice = None
    while choice !='3':
        choice = v.onboard()
        if choice == '1':
            status, username, password = v.create_account()
            if status:
                try:
                    m.account.create_user(username, password)
                except mysql.connector.errors.IntegrityError:
                    v.operation_failed(username)
                    continue
            else:
                v.operation_failed()
                continue
            v.operation_successsfull()
            onboard()
        elif choice == '2':
            status = False
            while True:
                username,password = v.login()
                status, user = m.account.login(username, password)
                if status:
                    v.operation_successsfull(username)
                    transactions(user)
        else:
            continue

def transactions(user):
    '''
    1. Search Stock
    2. Buy stock
    3. Sell stock
    4. View portfolio (owned stock, balance, profits/losses)
    5. Logout
    '''
    choice = None
    while choice != '4':
        choice = v.transactions_menu()
        if choice == '1':
            Stock = m.stock.search_stock()
            v.stock_info(Stock)
        elif choice == '2':
            v.buy_stock()
        elif choice == '3':
            v.sell_stock()
        elif choice == '4':
            v.view_portfolio(user)
        else:
            continue

def main():
    onboard()

if __name__=="__main__":
    main()


