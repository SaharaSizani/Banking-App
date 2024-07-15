import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import string
import re
from datetime import datetime

class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Upstreaming Banking App")
        self.geometry("400x300")
        self.configure(bg="lightblue")  # Set background color

        self.users = []  # Initialize users list

        # Load existing users data from file
        self.load_users_data()

        self.create_login_form()

    def load_users_data(self):
        try:
            with open('users.json', 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "No registered users found.")

    def create_login_form(self):
        self.label_pin = ttk.Label(self, text="Enter PIN:")
        self.label_pin.pack(pady=10)
        self.entry_pin = ttk.Entry(self, show="*")
        self.entry_pin.pack(pady=5)

        self.button_login = ttk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=10)

        self.button_register = ttk.Button(self, text="Register", command=self.register_window)
        self.button_register.pack(pady=5)

    def login(self):
        entered_pin = self.entry_pin.get()

        # Check if entered PIN matches any user's PIN
        for user in self.users:
            if user['pin'] == entered_pin:
                self.current_user = user
                self.show_main_menu()
                return

        # If no match found
        messagebox.showerror("Login Failed", "Invalid PIN. Please try again.")

    def register_window(self):
        self.withdraw()  # Hide login window
        register_window = RegistrationWindow(self, self.on_registration_success)
        register_window.geometry("400x600")
        register_window.title("Registration")
        register_window.mainloop()

    def on_registration_success(self, pin):
        # Reload users data after registration
    
        self.show_login()

    def show_main_menu(self):
        self.destroy()  # Close the current window
        # Create MainMenu instance with default accounts (can modify as per your database structure)
        # Example:
        account1 = BankAccount("141516", 1000.00)
        account2 = BankAccount("123456", 500.00)
        main_menu = MainMenu(account1, account2)
        main_menu.geometry("400x300")  # Example geometry
        main_menu.title(f"Welcome, {self.current_user['name']}!")
        main_menu.mainloop()

    def show_login(self):
        self.update()
        self.entry_pin.delete(0, tk.END)
        self.deiconify()

class RegistrationWindow(tk.Toplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success

        self.title("Registration")
        self.geometry("400x600")

        self.label_name = ttk.Label(self, text="Name and Surname:")
        self.label_name.pack(pady=5)
        self.entry_name = ttk.Entry(self)
        self.entry_name.pack(pady=5)

        self.label_password = ttk.Label(self, text="Generate Password:")
        self.label_password.pack(pady=5)
        self.entry_password = ttk.Entry(self)
        self.entry_password.pack(pady=5)

        self.label_create_pin = ttk.Label(self, text="Create New PIN:")
        self.label_create_pin.pack(pady=5)
        self.entry_create_pin = ttk.Entry(self, show="*")
        self.entry_create_pin.pack(pady=5)

        self.label_confirm_pin = ttk.Label(self, text="Confirm PIN:")
        self.label_confirm_pin.pack(pady=5)
        self.entry_confirm_pin = ttk.Entry(self, show="*")
        self.entry_confirm_pin.pack(pady=5)

        self.label_address = ttk.Label(self, text="Address:")
        self.label_address.pack(pady=5)
        self.entry_address = ttk.Entry(self)
        self.entry_address.pack(pady=5)

        self.label_email = ttk.Label(self, text="Email:")
        self.label_email.pack(pady=5)
        self.entry_email = ttk.Entry(self)
        self.entry_email.pack(pady=5)

        self.label_contact = ttk.Label(self, text="Contact Number:")
        self.label_contact.pack(pady=5)
        self.entry_contact = ttk.Entry(self)
        self.entry_contact.pack(pady=5)

        self.button_generate_password = ttk.Button(self, text="Generate Password", command=self.generate_password)
        self.button_generate_password.pack(pady=10)

        self.button_register = ttk.Button(self, text="Register", command=self.save_entries)
        self.button_register.pack(pady=10)

    def validate_email(self, email):
        # Basic email format validation
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            return False

    def validate_address(self, address):
        # Basic address format validation
        # Add your own validation logic here if needed
        if len(address) > 0:
            return True
        else:
            return False

    def validate_contact(self, contact):
        # Basic contact number validation (exactly 10 digits)
        if re.match(r"^\d{10}$", contact):
            return True
        else:
            return False


    def generate_password(self):
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, password)

    def save_entries(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        create_pin = self.entry_create_pin.get()
        confirm_pin = self.entry_confirm_pin.get()
        address = self.entry_address.get()
        email = self.entry_email.get()
        contact = self.entry_contact.get()

        if not (name and password and create_pin and confirm_pin and address and email and contact):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if create_pin != confirm_pin:
            messagebox.showerror("Error", "PINs do not match. Please try again.")
            return

        # Create a dictionary for user data
        user_data = {
            "name": name,
            "password": password,
            "pin": create_pin,
            "address": address,
            "email": email,
            "contact": contact
        }

        # Append new user data to the list
        self.parent.users.append(user_data)

        # Write updated users data back to file
        with open('users.json', 'w') as file:
            json.dump(self.parent.users, file, indent=4)

        messagebox.showinfo("Registration Successful", f"Registration successful for {name}. You can now log in with your PIN.")
        self.on_success(create_pin)
        self.destroy()


class MainMenu(tk.Tk):
    def __init__(self, account1=None, account2=None):
        super().__init__()
        self.title("Main Menu")
 
        # Store accounts
        self.account1 = account1
        self.account2 = account2
 
        # Style configuration for ttk
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.configure(bg="#f0f0f0")  # Set background color
 
        self.label_menu = ttk.Label(self, text="Please choose an option:")
        self.label_menu.pack(padx=10, pady=10, anchor=tk.W)
 
        # Buttons for different operations
        self.button_deposit = ttk.Button(self, text="Deposit", command=self.deposit_dialog)
        self.button_deposit.pack(padx=5, pady=5, fill=tk.X)
 
        self.button_withdraw = ttk.Button(self, text="Withdraw", command=self.withdraw_dialog)
        self.button_withdraw.pack(padx=5, pady=5, fill=tk.X)
 
        self.button_transfer = ttk.Button(self, text="Transfer", command=self.transfer_dialog)
        self.button_transfer.pack(padx=5, pady=5, fill=tk.X)
 
        self.button_balance = ttk.Button(self, text="Check Balance", command=self.check_balance)
        self.button_balance.pack(padx=5, pady=5, fill=tk.X)
 
        self.button_interest = ttk.Button(self, text="Deposit Interest", command=self.deposit_interest_dialog)
        self.button_interest.pack(padx=5, pady=5, fill=tk.X)
 
        self.button_view_transactions = ttk.Button(self, text="View Transactions", command=self.view_transactions)
        self.button_view_transactions.pack(padx=5, pady=5, fill=tk.X)
 
        # Button to exit the application
        self.button_exit = ttk.Button(self, text="Exit", command=self.quit)
        self.button_exit.pack(padx=5, pady=10, fill=tk.X)
 
    def deposit_dialog(self):
        dialog = TransactionDialog(self, "Deposit", self.account1.deposit)
        self.wait_window(dialog)
 
    def withdraw_dialog(self):
        dialog = TransactionDialog(self, "Withdraw", self.account1.withdraw)
        self.wait_window(dialog)
 
    def transfer_dialog(self):
        dialog = TransferDialog(self, self.account1, self.account2)
        self.wait_window(dialog)
 
    def check_balance(self):
        self.account1.check_balance()
 
    def deposit_interest_dialog(self):
        dialog = InterestDialog(self, self.account1.deposit_interest)
        self.wait_window(dialog)
 
    def view_transactions(self):
        self.account1.view_transactions()
 
class BankAccount:
    def __init__(self, account_number, balance=0.0):
        self.account_number = account_number
        self.balance = balance
        self.last_transaction_date = None
        self.transactions = []
 
    def deposit(self, amount):
        if amount > 0:
            deposit_fee = amount * 0.10  # 10% deposit fee
            total_deposit = amount - deposit_fee
            self.balance += total_deposit
            self.record_transaction(total_deposit, "Deposit")
            messagebox.showinfo("Deposit", f"Deposited R{amount:.2f} into account {self.account_number}. Deposit fee: R{deposit_fee:.2f}. New balance: R{self.balance:.2f}")
        else:
            messagebox.showerror("Error", "Invalid deposit amount.")
 
    def withdraw(self, amount):
        if amount > 0:
            self.apply_daily_withdrawal_charge()
            if self.balance >= amount:
                self.balance -= amount
                self.record_transaction(-amount, "Withdrawal")
                messagebox.showinfo("Withdrawal", f"Withdrew R{amount:.2f} from account {self.account_number}. New balance: R{self.balance:.2f}")
            else:
                messagebox.showerror("Error", f"Insufficient funds in account {self.account_number}.")
        else:
            messagebox.showerror("Error", "Invalid withdrawal amount.")
 
    def transfer(self, recipient_account, amount):
        if amount > 0:
            transfer_fee = 2.50  # Fixed transfer fee within the bank
            if recipient_account.startswith("14"):  # Example check for other bank account
                transfer_fee = 7.00  # Fixed transfer fee to other banks
            if self.balance >= amount + transfer_fee:
                self.balance -= (amount + transfer_fee)
                self.record_transaction(-amount - transfer_fee, f"Transferred R{amount:.2f} to {recipient_account}.")
                messagebox.showinfo("Transfer", f"Transferred R{amount:.2f} from account {self.account_number} to {recipient_account}.")
            else:
                messagebox.showerror("Error", f"Insufficient funds in account {self.account_number}.")
        else:
            messagebox.showerror("Error", "Invalid transfer amount.")
 
    def check_balance(self):
        messagebox.showinfo("Balance", f"Account {self.account_number} balance: R{self.balance:.2f}")
 
    def deposit_interest(self, interest_rate):
        if interest_rate > 0:
            interest_amount = self.balance * interest_rate
            self.balance += interest_amount
            self.record_transaction(interest_amount, "Interest")
            messagebox.showinfo("Interest", f"Deposited R{interest_amount:.2f} in interest into account {self.account_number}. New balance: R{self.balance:.2f}")
        else:
            messagebox.showerror("Error", "Invalid interest rate.")
 
    def view_transactions(self):
        if not self.transactions:
            messagebox.showinfo("Transactions", "No transactions recorded.")
        else:
            transaction_details = "\n".join(f"{t[0]}: {t[1]} R{t[2]:.2f}" for t in self.transactions)
            messagebox.showinfo("Transactions", transaction_details)
 
    def record_transaction(self, amount, description):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transactions.append((timestamp, description, amount))
 
    def apply_daily_withdrawal_charge(self):
        today = datetime.now().date()
        if self.last_transaction_date is None or self.last_transaction_date < today:
            self.last_transaction_date = today
            self.balance -= 1.00  # Daily withdrawal charge of R1.00
            self.record_transaction(-1.00, "Daily Withdrawal Charge")
 
class TransactionDialog(tk.Toplevel):
    def __init__(self, parent, operation, callback):
        super().__init__(parent)
        self.title(operation)
        self.geometry("300x200")
        self.operation = operation  # Store operation as an attribute
        self.callback = callback    # Callback function to execute on confirmation
 
        # Labels and Entry fields
        self.label_amount = ttk.Label(self, text="Amount:")
        self.label_amount.pack(pady=5)
        self.entry_amount = ttk.Entry(self)
        self.entry_amount.pack(pady=5)
 
        # Button to confirm transaction
        self.button_confirm = ttk.Button(self, text="Confirm", command=self.confirm_transaction)
        self.button_confirm.pack(pady=10)
 
    def confirm_transaction(self):
        try:
            amount = float(self.entry_amount.get())
            self.callback(amount)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
class TransferDialog(tk.Toplevel):
    def __init__(self, parent, account_from, account_to):
        super().__init__(parent)
        self.title("Transfer")
        self.account_from = account_from
        self.account_to = account_to
        self.label_amount = ttk.Label(self, text="Enter amount to transfer:")
        self.label_amount.pack(padx=10, pady=10)
        self.entry_amount = ttk.Entry(self)
        self.entry_amount.pack(padx=10, pady=10)
        # Dropdown for bank selection
        self.label_bank_name = ttk.Label(self, text="Select recipient's bank:")
        self.label_bank_name.pack(padx=10, pady=5)
        self.banks = ["Capitec", "Absa", "Standard Bank", "Nedbank", "Fnb", "Bidvest"]  # Replace with your bank list
        self.bank_selection = ttk.Combobox(self, values=self.banks, state="readonly")
        self.bank_selection.pack(padx=10, pady=5)
        self.bank_selection.bind("<<ComboboxSelected>>", self.update_branch_code)
        # Entry field for branch code
        self.label_branch_code = ttk.Label(self, text="Recipient's branch code:")
        self.label_branch_code.pack(padx=10, pady=5)
        self.entry_branch_code = ttk.Entry(self)
        self.entry_branch_code.pack(padx=10, pady=5)
        # Entry field for account number
        self.label_account_number = ttk.Label(self, text="Recipient's account number:")
        self.label_account_number.pack(padx=10, pady=5)
        self.entry_account_number = ttk.Entry(self)
        self.entry_account_number.pack(padx=10, pady=5)
        self.button_ok = ttk.Button(self, text="OK", command=self.transfer)
        self.button_ok.pack(padx=10, pady=10)
        self.button_print_receipt = ttk.Button(self, text="Print Receipt", command=self.print_receipt)
        self.button_print_receipt.pack(padx=10, pady=5)
        self.button_print_receipt.config(state=tk.DISABLED)  # Disable initially
    def update_branch_code(self, event=None):
        selected_bank = self.bank_selection.get()
        if selected_bank == "Capitec":
            self.entry_branch_code.delete(0, tk.END)
            self.entry_branch_code.insert(0, "470010")  # Replace with actual Capitec branch code
        elif selected_bank == "Absa":
            self.entry_branch_code.delete(0, tk.END)
            self.entry_branch_code.insert(0, "632005")  # Replace with actual Absa branch code
        elif selected_bank == "Standard Bank":
            self.entry_branch_code.delete(0, tk.END)
            self.entry_branch_code.insert(0, "051001")  # Replace with actual Standard Bank branch code
        elif selected_bank == "Nedbank":
            self.entry_branch_code.delete(0, tk.END)
            self.entry_branch_code.insert(0, "198765")  # Replace with actual Nedbank branch code
        elif selected_bank == "Fnb":
            self.entry_branch_code.delete(0, tk.END)
            self.entry_branch_code.insert(0, "250655")  # Replace with actual FNB branch code
        elif selected_bank == "Bidvest":
            self.entry_branch_code.delete(0, tk.END)
            self.entry_branch_code.insert(0, "462005")  # Replace with actual Bidvest branch code
    def transfer(self):
        try:
            amount = float(self.entry_amount.get())
            account_number = self.entry_account_number.get().strip()  # Retrieve and strip any extra spaces
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a valid amount greater than zero.")
                return
            if not account_number:
                messagebox.showerror("Error", "Please enter recipient's account number.")
                return
            recipient_bank_name = self.bank_selection.get()
            branch_code = self.entry_branch_code.get()
            # Validate if the account number is valid in a real scenario
            # For demonstration, we assume any account number is valid
            # Replace this with actual validation logic in a real application
            # Display confirmation dialog
            confirmation_message = (
                f"Transfer Details:\n"
                f"Bank Name: {recipient_bank_name}\n"
                f"Branch Code: {branch_code}\n"
                f"Account Number: {account_number}\n"
                f"Amount: ${amount:.2f}\n\n"
                f"Proceed with transfer?"
            )
            if messagebox.askyesno("Confirm Transfer", confirmation_message):
                # For now, assuming direct transfer within the same bank
                self.account_from.withdraw(amount)
                self.account_to.deposit(amount)
                messagebox.showinfo("Transfer", f"Transfer of ${amount:.2f} successful.")
                self.parent.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    def print_receipt(self):
        amount = float(self.entry_amount.get())
        recipient_bank_name = self.bank_selection.get()
        branch_code = self.entry_branch_code.get()
        receipt_message = (
            f"Transfer Details:\n"
            f"Bank Name: {recipient_bank_name}\n"
            f"Branch Code: {branch_code}\n"
            f"Amount: ${amount:.2f}\n"
            f"Date and Time: {datetime.now()}\n"
            f"Thank you for using our services!"
        )
        messagebox.showinfo("Receipt", receipt_message)
    def transfer(self):
        try:
            amount = float(self.entry_amount.get())
            if amount > 0:
                self.account_from.withdraw(amount)
                self.account_to.deposit(amount)
                messagebox.showinfo("Transfer", f"Transfer of R{amount:.2f} successful.")
                self.parent.destroy()
            else:
                messagebox.showerror("Error", "Please enter a valid amount.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
class InterestDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Deposit Interest")
        self.geometry("300x200")
        self.callback = callback    # Callback function to execute on confirmation
        # Labels and Entry fields
        self.label_interest_rate = ttk.Label(self, text="Interest Rate:")
        self.label_interest_rate.pack(pady=5)
        self.entry_interest_rate = ttk.Entry(self)
        self.entry_interest_rate.pack(pady=5)
        # Button to confirm interest deposit
        self.button_confirm = ttk.Button(self, text="Confirm", command=self.confirm_deposit_interest)
        self.button_confirm.pack(pady=10)
    def confirm_deposit_interest(self):
        try:
            interest_rate = float(self.entry_interest_rate.get())
            self.callback(interest_rate)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid interest rate.")
    def exit_application(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            print("Thank you for using our banking app. Goodbye!")
            self.destroy()  # Show the login window of the parent
def main():
    app = BankingApp()
    app.geometry("400x300")  # Set initial window size
    app.mainloop()

if __name__ == "__main__":
    main()
