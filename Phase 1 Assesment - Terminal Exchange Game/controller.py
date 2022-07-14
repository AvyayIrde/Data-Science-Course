import model as m
import view as v

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
    while choice !=3:
        choice = v.onboard()
        if choice == 1:
            m.

