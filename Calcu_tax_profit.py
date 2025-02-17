import tkinter as tk
from tkinter import messagebox

class FamilyAccount:
    def __init__(self):
        self.siblings = []  # List to store sibling data
        self.profit_percentage = 5  # Default profit percentage
        self.tax_percentage = 10   # Default tax percentage

    def add_sibling(self, name, amount):
        """Add or update a sibling's data."""
        for sibling in self.siblings:
            if sibling['name'] == name:
                sibling['amount'] = amount
                return
        self.siblings.append({"name": name, "amount": amount, "profit": 0, "tax": 0})

    def calculate_profit_tax(self):
        """Calculate profit and tax for each sibling."""
        for sibling in self.siblings:
            sibling['profit'] = sibling['amount'] * (self.profit_percentage / 100)
            sibling['tax'] = sibling['profit'] * (self.tax_percentage / 100)

    def get_total_profit(self):
        """Calculate the total profit."""
        return sum(sibling['profit'] for sibling in self.siblings)

    def get_total_tax(self):
        """Calculate the total tax deductions."""
        return sum(sibling['tax'] for sibling in self.siblings)

    def get_net_balance(self):
        """Get net balance after tax deductions."""
        return self.get_total_profit() - self.get_total_tax()

    def update_percentages(self, new_profit_percentage, new_tax_percentage):
        """Update profit and tax percentages."""
        self.profit_percentage = new_profit_percentage
        self.tax_percentage = new_tax_percentage

class FamilyAccountGUI:
    def __init__(self, root, family_account):
        self.family_account = family_account
        self.root = root
        self.root.title("Family Bank Manager")

        # Profit and Tax percentage fields
        tk.Label(root, text="Profit %:").grid(row=0, column=0)
        self.profit_entry = tk.Entry(root)
        self.profit_entry.insert(0, str(self.family_account.profit_percentage))
        self.profit_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Tax %:").grid(row=1, column=0)
        self.tax_entry = tk.Entry(root)
        self.tax_entry.insert(0, str(self.family_account.tax_percentage))
        self.tax_entry.grid(row=1, column=1)

        tk.Button(root, text="Update %", command=self.update_percentages).grid(row=2, column=0, columnspan=2)

        # Sibling Details
        tk.Label(root, text="Name:").grid(row=3, column=0)
        self.sibling_name_entry = tk.Entry(root)
        self.sibling_name_entry.grid(row=3, column=1)

        tk.Label(root, text="Amount:").grid(row=4, column=0)
        self.sibling_amount_entry = tk.Entry(root)
        self.sibling_amount_entry.grid(row=4, column=1)

        tk.Button(root, text="Add/Update Sibling", command=self.add_sibling).grid(row=5, column=0, columnspan=2)

        # Display Sibling Data
        tk.Label(root, text="Siblings Data:").grid(row=6, column=0)
        self.sibling_listbox = tk.Listbox(root, width=50)
        self.sibling_listbox.grid(row=7, column=0, columnspan=2)

        # Calculate Profit and Tax
        tk.Button(root, text="Calculate", command=self.calculate_profit_tax).grid(row=8, column=0, columnspan=2)

        self.total_profit_label = tk.Label(root, text="Total Profit: 0 PKR")
        self.total_profit_label.grid(row=9, column=0)

        self.total_tax_label = tk.Label(root, text="Total Tax: 0 PKR")
        self.total_tax_label.grid(row=10, column=0)

        self.net_balance_label = tk.Label(root, text="Net Balance: 0 PKR")
        self.net_balance_label.grid(row=11, column=0)

    def update_percentages(self):
        try:
            new_profit_percentage = float(self.profit_entry.get())
            new_tax_percentage = float(self.tax_entry.get())
            self.family_account.update_percentages(new_profit_percentage, new_tax_percentage)
            messagebox.showinfo("Success", "Percentages updated successfully.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid percentages.")

    def add_sibling(self):
        sibling_name = self.sibling_name_entry.get()
        try:
            sibling_amount = float(self.sibling_amount_entry.get())
            self.family_account.add_sibling(sibling_name, sibling_amount)
            self.refresh_list()
            self.sibling_name_entry.delete(0, tk.END)
            self.sibling_amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def calculate_profit_tax(self):
        self.family_account.calculate_profit_tax()
        total_profit = self.family_account.get_total_profit()
        total_tax = self.family_account.get_total_tax()
        net_balance = self.family_account.get_net_balance()
        
        self.total_profit_label.config(text=f"Total Profit: {total_profit:.2f} PKR")
        self.total_tax_label.config(text=f"Total Tax: {total_tax:.2f} PKR")
        self.net_balance_label.config(text=f"Net Balance: {net_balance:.2f} PKR")
        self.refresh_list()

    def refresh_list(self):
        self.sibling_listbox.delete(0, tk.END)
        for sibling in self.family_account.siblings:
            self.sibling_listbox.insert(tk.END, f"{sibling['name']}: {sibling['amount']} PKR, Profit: {sibling['profit']:.2f}, Tax: {sibling['tax']:.2f}")

if __name__ == "__main__":
    family_account = FamilyAccount()
    root = tk.Tk()
    gui = FamilyAccountGUI(root, family_account)
    root.mainloop()
