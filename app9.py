from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)

# Connect to the AWS DynamoDB database
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('bank_accounts')

class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: {amount}")
        table.update_item(
            Key={
                'account_number': self.account_number
            },
            UpdateExpression='SET balance = :val1, transactions = :val2',
            ExpressionAttributeValues={
                ':val1': self.balance,
                ':val2': self.transactions
            }
        )

    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: {amount}")
            table.update_item(
                Key={
                    'account_number': self.account_number
                },
                UpdateExpression='SET balance = :val1, transactions = :val2',
                ExpressionAttributeValues={
                    ':val1': self.balance,
                    ':val2': self.transactions
                }
            )
        else:
            self.transactions.append(f"Insufficient funds for withdrawal: {amount}")
            table.update_item(
                Key={
                    'account_number': self.account_number
                },
                UpdateExpression='SET transactions = :val1',
                ExpressionAttributeValues={
                    ':val1': self.transactions
                }
            )

    def display_balance(self):
        return f"Balance: {self.balance}"

    def display_transactions(self):
        return "\n".join(self.transactions)

@app.route("/")
def index():
    return redirect(url_for("display_balance"))

@app.route("/balance", methods=["GET", "DELETE"])
def display_balance():
    if request.method == "DELETE":
        account_number = request.args.get('account_number')
        account = BankAccount(account_number)
        account.balance = 0
        account.transactions = []
        table.update_item(
            Key={
                'account_number': account_number
            },
            UpdateExpression='SET balance = :val1, transactions = :val2',
            ExpressionAttributeValues={
                ':val1': account.balance,
                ':val2': account.transactions
            }
        )
        return redirect(url_for("display_balance"))
    account_number = request.args.get('account_number')
    account = BankAccount(account_number)
    response = table
