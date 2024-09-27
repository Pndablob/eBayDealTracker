import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, colorchooser
import os

window = tk.Tk()

# Messages
messagebox.showinfo("Information", "Informative message")
messagebox.showerror("Error", "Error message")
messagebox.showwarning("Warning", "Warning message")

# Selections
answer = messagebox.askokcancel("Question", "Do you want to open this file?")
print(answer)
answer = messagebox.askretrycancel("Question", "Do you want to try that again?")
print(answer)
answer = messagebox.askyesno("Question", "Do you like Python?")
print(answer)
answer = messagebox.askyesnocancel("Question", "Continue Playing?")
print(answer)

# Single Value User Input
first_name = simpledialog.askstring("Input", "What is your first name?", parent=window)
if first_name is not None:
    print(f"Hello {first_name}")
else:
    print(f"You don't have a first name?")

age = simpledialog.askinteger("Input", "What is your age", parent=window, minvalue=0, maxvalue=150)
if age is not None:
    print(f"Hello {first_name}. You are {age} years old")
else:
    print("You don't have an age?")

salary = simpledialog.askfloat("Input", "What is your salary?", parent=window, minvalue=0.0, maxvalue=1000000.0)
if salary is not None:
    print(f"Hello {first_name}. You are {age} years old and your salary is {salary}")
else:
    print("You're broke")

# File Chooser
filetypes = [('all files', ".*"), ('text files', ".txt"), ('pdf files', ".pdf")]

answer = filedialog.askdirectory(parent=window, initialdir=os.getcwd(), title="Please select a folder:")
print(answer)
answer = filedialog.askopenfilename(parent=window, initialdir=os.getcwd(), title="Please select a file:", filetypes=filetypes)
print(answer)
answer = filedialog.askopenfilenames(parent=window, initialdir=os.getcwd(), title="Please select one or more file", filetypes=filetypes)
print(answer)
answer = filedialog.asksaveasfilename(parent=window, initialdir=os.getcwd(), title="Please select a file name for saving:", filetypes=filetypes)
print(answer)

# Choosing Colors
rgb_color, web_color = colorchooser.askcolor(parent=window, initialcolor=(255, 0, 0))


window.mainloop()
