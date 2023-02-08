import tkinter as tk

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: {amount}")

    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: {amount}")
        else:
            self.transactions.append(f"Insufficient funds for withdrawal: {amount}")

    def display_balance(self):
        return f"Balance: {self.balance}"

    def display_transactions(self):
        return "\n".join(self.transactions)

class BankApp(tk.Tk):
    def __init__(self, account):
        tk.Tk.__init__(self)
        self.title("Bank App")
        self.account = account

        self.balance_label = tk.Label(self, text=self.account.display_balance())
        self.balance_label.pack()

        self.transactions_label = tk.Label(self, text=self.account.display_transactions(), wraplength=300)
        self.transactions_label.pack()

        self.deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack()

    def deposit(self):
        deposit_amount = int(tk.simpledialog.askstring("Deposit", "Enter deposit amount:"))
        self.account.deposit(deposit_amount)
        self.balance_label.config(text=self.account.display_balance())
        self.transactions_label.config(text=self.account.display_transactions())

    def withdraw(self):
        withdrawal_amount = int(tk.simpledialog.askstring("Withdrawal", "Enter withdrawal amount:"))
        self.account.withdraw(withdrawal_amount)
        self.balance_label.config(text=self.account.display_balance())
        self.transactions_label.config(text=self.account.display_transactions())

if __name__ == "__main__":
    account = BankAccount(100)
    app = BankApp(account)
    app.mainloop()
