import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox as ComboBox

# ---TKINTER WINDOW---

# ---main frame---
main_frame = tk.Tk()
main_frame.geometry("400x500")
main_frame.title("PERSONAL EXPENSE TRACKER")
main_frame.config(bg="lightblue", pady=20, padx=20)
heading = Label(main_frame, text="PERSONAL EXPENSE TRACKER", font=("Arial", 16), bg="lightblue")
heading.pack(pady=10)

# date label/entry
date_l = Label(main_frame, text="DATE (in dd/mm/yyyy)", bg="lightblue")
date_l.pack(pady=5)
date_e1 = datetime.date.today().strftime("%d/%m/%Y")
date_entry = Entry(main_frame)
date_entry.insert(0, date_e1)
date_entry.pack(pady=5)

# category label/entry
category_l = Label(main_frame, text="CATEGORY", bg="lightblue")
category_l.pack(pady=5)
category_e = ComboBox(main_frame, values=["Food", "Transport", "Entertainment", "Shopping", "Other"], state="readonly")
category_e.set("Select Category")
category_e.pack(pady=5)

# description label/entry
description_l = Label(main_frame, text="DESCRIPTION", bg="lightblue")
description_l.pack(pady=5)
description_e = Entry(main_frame)
description_e.pack(pady=5)

# amount label/entry
amount_l = Label(main_frame, text="AMOUNT (in Rs.)", bg="lightblue")
amount_l.pack(pady=5)
amount_e = Entry(main_frame)
amount_e.pack(pady=5)

# submit button
def add_expense():
    date = date_entry.get()
    category = category_e.get()
    description = description_e.get()
    amount = amount_e.get()
    amount = float(amount)
    save1 = messagebox.askyesno("SAVE", "Do you want to save this expense?")
    save2 = messagebox.askyesno("CONFIRM", "Are you sure you want to save this expense?")
    if save1 and save2:
        try:
            if not date or not category or not description or not amount:
                messagebox.showerror("ERROR", "All fields are required!")
            elif datetime.datetime.strptime(date, "%d/%m/%Y") > datetime.datetime.now():
                messagebox.showerror("ERROR", "Date is invalid!")
            elif category == "Select Category":
                messagebox.showerror("ERROR", "Please select a valid category!")
            elif description.strip() == "":
                messagebox.showerror("ERROR", "Description cannot be empty!")
            elif amount <= 0:
                messagebox.showerror("ERROR", "Amount is invalid!")
            else:
                messagebox.showinfo("SAVED", "Expense saved successfully!")
                data = {"Date": [date],"Category": [category],"Description": [description],"Amount": [amount]}
                df = pd.DataFrame(data)
                df.to_csv(r"C:\Users\Gaurav\Downloads\expenses.csv", mode="a", index=False, header=not pd.io.common.file_exists(r"C:\Users\Gaurav\Downloads\expenses.csv"))
                date_entry.delete(0, END)
                category_e.set("Select Category")
                description_e.delete(0, END)
                amount_e.delete(0, END)
                
        except Exception as e:
            messagebox.showerror("ERROR", f"An error occurred: {e}")
            
    else:
        messagebox.showinfo("CANCELLED", "Expense not saved.")    
submit_b = Button(main_frame, text="ADD EXPENSE", bg="lightgreen", command=add_expense)
submit_b.pack(pady=20)

# visualization by date & category options
Label(main_frame, text="VISUALIZE EXPENSES", bg="lightblue").pack(pady=10)
viz = ComboBox(main_frame, values=['By date - line graph','By category - line graph','By category - pie chart'], state="readonly")
viz.set("Select Option")
viz.pack(pady=5)

def show_expenses():
    viz_option = viz.get()
    if viz_option == "Select Option":
        messagebox.showerror("ERROR", "Please select a valid option!")
    else:
        viz.set("Select Option")
        try:
            df = pd.read_csv(r"C:\Users\Gaurav\Downloads\expenses.csv")
            if df.empty:
                messagebox.showinfo("NO DATA", "No expenses to show!")
                return
            df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
            if viz_option == 'By date - line graph':
                df.groupby('Date')['Amount'].sum().plot(kind='line', marker='o', color='blue')
                plt.title("Expenses Over Time")
                plt.xlabel("Date")
                plt.ylabel("Total Amount (Rs.)")
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            elif viz_option == 'By category - line graph':
                df.groupby('Category')['Amount'].sum().plot(kind='line', marker='o', color='green')
                plt.title("Expenses by Category")
                plt.xlabel("Category")
                plt.ylabel("Total Amount (Rs.)")
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            elif viz_option == 'By category - pie chart':
                df.groupby('Category')['Amount'].sum().plot(kind='pie', autopct='%1.1f%%', startangle=90)
                plt.title("Expenses Distribution by Category")
                plt.ylabel("")
                plt.show()
        except Exception as e:
            messagebox.showerror("ERROR", f"An error occurred: {e}")
Button(main_frame, text="SHOW", bg="lightgreen", command=show_expenses).pack(pady=5)

Button(main_frame, text="EXIT", bg="red", command=main_frame.destroy).place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)
main_frame.mainloop()