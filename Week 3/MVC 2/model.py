from random import randrange
import json

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
        acc_no = randrange(acc_start,acc_end)
        with open('data/bank.json','r') as file:
            data = json.load(file)
        while acc_no in data:
            acc_no = randrange(acc_start,acc_end)
        acc = account(acc_no, username, password)
        acc.save()
        return acc

    def save(self):
        with open('data/bank.json','r') as file:
            data = json.load(file) #json to dict
        data[self.acc_no] = {'username':self.username, 'password':self.password, 'balance':self.balance}

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
    def login(cls, acc_no, password):
        with open('data/bank.json','r') as file:
            data = json.load(file)
        if acc_no in data and data[acc_no]['password'] == password:
            username = data[acc_no]['username']
            balance = data[acc_no]['balance']
            acc = account(acc_no,username,password,balance)
