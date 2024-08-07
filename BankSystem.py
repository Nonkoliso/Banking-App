import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog, PhotoImage
import string
import random
from dbinit import DB  # Import the DB class from dbinit.py

class BankSystem:
    def __init__(self, data_file='bank_system.txt'):  # Update the default file name
        self.db = DB(data_file)  # Use the DB class for database operations

    def generate_ac_no(self, name, country):
        name_char_vals = [ord(i) for i in name]
        sum_name_char_vals = sum(name_char_vals)
        base_num = 90036900100000
        ac_no = country[0:2].upper() + str(base_num + sum_name_char_vals)
        return ac_no

    def sign_up(self, name, country, contact, email, password, gender):
        ac_num = self.generate_ac_no(name, country)
        data = self.db.read_data()  # Use the DB class method
        for record in data:
            if record[3] == email:
                return False, "Email already used!"

        new_user = [name, country, contact, email, password, ac_num, '0', gender]
        data.append(new_user)
        self.db.write_data(data)  # Use the DB class method
        return True, "Account created successfully."

    def check_bal(self, ac_no):
        return self.db.check_bal(ac_no)  # Use the DB class method

    def update_balance(self, ac_no, new_balance):
        self.db.update_balance(ac_no, new_balance)  # Use the DB class method

    def add_money(self, ac_no, amount):
        balance = self.check_bal(ac_no)
        new_balance = balance + amount
        self.update_balance(ac_no, new_balance)
        return new_balance

    def withdraw(self, ac_no, amount):
        balance = self.check_bal(ac_no)
        if balance >= amount:
            new_balance = balance - amount
            self.update_balance(ac_no, new_balance)
            return new_balance
        return False

    def sign_in(self, email, password):
        data = self.db.read_data()  # Use the DB class method
        for record in data:
            if record[3] == email and record[4] == password:
                return True, record
        return False, "Account doesn't exist or wrong credentials."

    def generate_password(self, length=12):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800")
        self.root.title("Pocket Bank")
        self.bank_system = BankSystem('bank_system.txt')  # Use the updated BankSystem class
        self.logged_in_user = None

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.root.configure(bg='#fff')

        try:
            image = PhotoImage(file="images/banking-apps_meta_resized.png")
            image_label = tk.Label(self.root, image=image)
            image_label.image = image
            image_label.pack()
        except Exception as e:
            print(f"Error loading image: {e}")

        tk.Label(self.root, text="User Login", font="poppins", background="#fff").pack(pady=10)
        tk.Label(self.root, text="Email", font="poppins", background="#fff").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        tk.Label(self.root, text="Password", font="poppins", background="#fff").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        tk.Button(self.root, text="Sign In", background="#8DD9CC", activebackground="orange", font="poppins", command=self.sign_in).pack(pady=10)
        tk.Button(self.root, text="Create an Account", background="#8DD9CC", activebackground="orange", font="poppins", borderwidth=8, command=self.create_signup_screen).pack()

    def create_signup_screen(self):
        self.clear_screen()

        self.root.configure(bg='#8DD9CC')


        tk.Label(self.root, text="Sign Up", font=("poppins"), background="#8DD9CC").pack(pady=10)
        tk.Label(self.root, text="Name", background="#8DD9CC").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Label(self.root, text="Country", background="#8DD9CC").pack()
        self.country_entry = tk.Entry(self.root)
        self.country_entry.pack()
        tk.Label(self.root, text="Contact No", background="#8DD9CC").pack()
        self.contact_entry = tk.Entry(self.root)
        self.contact_entry.pack()
        tk.Label(self.root, text="Email", background="#8DD9CC").pack()
        self.email_signup_entry = tk.Entry(self.root)
        self.email_signup_entry.pack()

        tk.Label(self.root, text="Gender", background="#8DD9CC").pack()
        self.gender_var = tk.StringVar(value="Male")
        tk.Radiobutton(self.root, text="Male", background="#8DD9CC", variable=self.gender_var, value="Male").pack()
        tk.Radiobutton(self.root, text="Female", background="#8DD9CC", variable=self.gender_var, value="Female").pack()

        tk.Label(self.root, text="Password", background="#8DD9CC").pack()
        self.password_signup_entry = tk.Entry(self.root, show='*')
        self.password_signup_entry.pack()

        self.random_password_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Use Random Password", background="#8DD9CC", variable=self.random_password_var).pack()

        tk.Button(self.root, text="Sign Up",background="#fff", activebackground="orange", font=("poppins"), command=self.sign_up).pack(pady=10)
        tk.Button(self.root, text="Back", background="#fff", activebackground="orange", borderwidth=8, font=("poppins"), command=self.create_login_screen).pack()

    def create_main_menu(self):
        self.clear_screen()
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        
        self.root.configure(bg='#8DD9CC')


        greeting = "Mr." if self.logged_in_user[7] == "Male" else "Ms."

        tk.Label(self.root, text=f"Welcome {greeting} {self.logged_in_user[0].upper()}", font=("poppins"), background="#8DD9CC").grid(row=0, column=1, pady=10, sticky='ew')
        tk.Label(self.root, text=f"A/C No.: {self.logged_in_user[5]}", background="#8DD9CC").grid(row=1, column=1, pady=5, sticky='ew')

        tk.Button(self.root, text="Check Balance", background="#fff", activebackground="orange", font=("poppins"), command=self.check_balance).grid(row=2, column=1, pady=5, sticky='ew')
        tk.Button(self.root, text="Add Money", background="#fff", activebackground="orange", font=("poppins"), command=self.add_money).grid(row=3, column=1, pady=5, sticky='ew')
        tk.Button(self.root, text="Withdraw Money", background="#fff", activebackground="orange", font=("poppins"), command=self.withdraw_money).grid(row=4, column=1, pady=5, sticky='ew')
        tk.Button(self.root, text="Sign Out",background="#fff", activebackground="orange",borderwidth=8,  font=("poppins"), command=self.sign_out).grid(row=5, column=1, pady=20, sticky='ew')

    def sign_in(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        success, result = self.bank_system.sign_in(email, password)
        if success:
            self.logged_in_user = result
            self.create_main_menu()
        else:
            messagebox.showerror("Error", result)

    def sign_up(self):
        name = self.name_entry.get()
        country = self.country_entry.get()
        contact = self.contact_entry.get()
        email = self.email_signup_entry.get()
        gender = self.gender_var.get()

        if self.random_password_var.get():
            password = self.bank_system.generate_password()
            messagebox.showinfo("Generated Password", f"Your generated password is: {password}")
        else:
            password = self.password_signup_entry.get()

        success, message = self.bank_system.sign_up(name, country, contact, email, password, gender)
        if success:
            messagebox.showinfo("Success", message)
            self.create_login_screen()
        else:
            messagebox.showerror("Error", message)

    def transaction_prompt(self):
        balance = self.bank_system.check_bal(self.logged_in_user[5])
        if messagebox.askyesno("Transaction", "Would you like to make a transaction?"):
            if messagebox.askyesno("Transaction Type", "Would you like to make a deposit? (No for withdrawal)"):
                self.transaction_screen(balance, "Deposit", self.bank_system.add_money)
            else:
                self.transaction_screen(balance, "Withdraw", self.bank_system.withdraw)
        else:
            self.create_main_menu()

    def transaction_screen(self, balance, transaction_type, transaction_func):
        self.clear_screen()
        
        self.root.configure(bg='#8DD9CC')


        tk.Label(self.root, text=f"Current Balance: {balance}", font=("Arial", 14), background="#8DD9CC").pack(pady=10)

        tk.Label(self.root, text=transaction_type, font=("Arial", 18), background="#8DD9CC").pack(pady=10)
        tk.Label(self.root, text="Amount", background="#8DD9CC").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        def perform_transaction():
            try:
                amount = float(self.amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")
                new_balance = transaction_func(self.logged_in_user[5], amount)
                if new_balance is not False:
                    messagebox.showinfo("Success", f"Transaction Successful. New balance: {new_balance}")
                else:
                    messagebox.showerror("Error", "Transaction Failed. Insufficient funds.")
            except ValueError:
                messagebox.showerror("Error", "You provided an invalid input.")
            self.create_main_menu()

        tk.Button(self.root, text="Submit",background="#8DD9CC", activebackground="orange", font=("poppins"), command=perform_transaction).pack(pady=10)
        tk.Button(self.root, text="Back", background="#8DD9CC", activebackground="orange", font=("poppins"), borderwidth=8, command=self.create_main_menu).pack()

    def check_balance(self):
        balance = self.bank_system.check_bal(self.logged_in_user[5])
        messagebox.showinfo("Balance", f"Your current balance is: {balance}")

    def add_money(self):
        self.transaction_screen(self.bank_system.check_bal(self.logged_in_user[5]), "Deposit", self.bank_system.add_money)

    def withdraw_money(self):
        self.transaction_screen(self.bank_system.check_bal(self.logged_in_user[5]), "Withdraw", self.bank_system.withdraw)

    def sign_out(self):
        self.logged_in_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
