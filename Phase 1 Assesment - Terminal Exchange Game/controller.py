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
    4. Or type secert code to enter admin menu
    '''
    v.clear()
    choice = None
    while choice !='3':
        choice = v.onboard()
        v.clear()
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
            username,password = v.login()
            status, user = m.account.login(username, password)
            if status:
                v.clear()
                v.operation_successsfull(username)
                transactions(user)
            else:
                v.operation_failed()
                continue
        elif choice == '3':
            exit()
        elif choice == '725969':
            admin()
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
    while choice != '5':
        choice = v.transactions_menu()
        v.clear()
        if choice == '1':
            keyword = v.search_stock()
            status, Stock = m.stock.search_stock(keyword)
            if status:
                v.stock_info(Stock)
            else:
                v.operation_failed()
        elif choice == '2':
            symbol = v.trade_stock()
            status, Stock = m.stock.search_stock(symbol)
            if status:
                status = False
                quantity = v.stock_quantity(Stock, user)
                trade = m.trades(user, Stock, quantity)
                status = trade.trade_stock(action = 'buy')
                if status:
                    v.operation_successsfull()
                else:
                    v.operation_failed()
            else:
                v.operation_failed()
        elif choice == '3':
            symbol = v.trade_stock()
            status, Stock = m.stock.search_stock(symbol)
            if status:
                status = False
                quantity = v.stock_quantity(Stock, user)
                trade = m.trades(user, Stock, quantity)
                status = trade.trade_stock(action = 'sell')
                if status:
                    v.operation_successsfull()
                else:
                    v.operation_failed()
            else:
                v.operation_failed()
        elif choice == '4':
            portfolio = m.trades.portfolio(user)
            v.view_portfolio(user, portfolio)
        elif choice == '5':
            onboard()
        else:
            continue

def admin():
    '''
    1. View all users
    2. View all stocks in database
    3. View all trades
    4. Logout
    '''
    choice = None
    while choice != '4':
        choice = v.admin_menu()
        v.clear()
        if choice == '1':
            users = m.account.get_users()
            v.view_users(users)
        elif choice == '2':
            stocks = m.stock.get_stocks()
            v.view_stocks(stocks)
        elif choice == '3':
            trades = m.trades.get_trades()
            v.view_trades(trades)
        elif choice == '4':
            onboard()
        else:
            continue

def main():
    onboard()

if __name__=="__main__":
    main()


