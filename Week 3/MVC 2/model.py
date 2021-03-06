from random import randrange
import json
import bcrypt
import base64

acc_start = 100000000 # to generate account number for every user
acc_end = 1000000000

class account:
    def __init__(self, acc_no, username, password, balance = 0):
        self.acc_no = acc_no
        self.username = username
        self.password = password
        self.balance = balance

    @classmethod
    def create_acc(cls, username, password):
        status = True
        acc_no = randrange(acc_start,acc_end)
        with open('data/bank.json','r') as file:
            data = json.load(file)
        while acc_no in data:
            acc_no = randrange(acc_start,acc_end)
        acc = account(acc_no, username, password) # cls(acc_no, username, password)
        acc.save() 
        return status,acc

    def save(self):
        with open('data/bank.json','r') as file:
            data = json.load(file) #json to dict
        data[self.acc_no] = {'username':self.username, 'password':base64.b64encode(bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())).decode(), 'balance':self.balance} #base64.b64encode(bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())).decode()

        with open('data/bank.json','w') as file:
            json.dump(data,file,indent = 4)
        return

    def deposit_money(self,deposit):
        self.balance += deposit
        self.save()
        return True
    
    def withdraw_money(self,withdraw):
        if withdraw < self.balance:
            self.balance -= withdraw
        self.save()
        return True

    @classmethod
    def login(cls, username, password):
        status = False
        acc = None
        with open('data/bank.json','r') as file:
            data = json.load(file)
        for acc_no in data:
            if data[acc_no]['username'] == username and bcrypt.checkpw(password.encode(), base64.b64decode(data[acc_no]['password'].encode())):
                username = data[acc_no]['username']
                balance = data[acc_no]['balance']
                acc = account(acc_no,username,password,balance) # cls(acc_no, username, password)
                status = True
        return status,acc
                
            
                
