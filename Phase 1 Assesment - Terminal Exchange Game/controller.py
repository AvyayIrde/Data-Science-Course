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
    status = False
    while choice != '4':
        choice = v.transactions_menu()
        if choice == '1':
            keyword = v.search_stock()
            Stock = m.stock.search_stock(keyword)
            v.stock_info(Stock)
        elif choice == '2':
            symbol = v.trade_stock()
            Stock = m.stock.search_stock(symbol)
            quantity = v.stock_quantity(Stock, user)
            trade = m.trades(user, Stock, quantity)
            status = trade.trade_stock(action = 'buy')
            if status:
                v.operation_successsfull()
            else:
                v.operation_failed()
        elif choice == '3':
            symbol = v.trade_stock()
            Stock = m.stock.search_stock(symbol)
            quantity = v.stock_quantity(Stock, user)
            trade = m.trades(user, Stock, quantity)
            status = trade.trade_stock(action = 'sell')
            if status:
                v.operation_successsfull()
            else:
                v.operation_failed()
        elif choice == '4':
            Stocks = m.trades.portfolio(user)
            v.view_portfolio(user, Stocks)
        else:
            continue

def main():
    onboard()

if __name__=="__main__":
    main()


