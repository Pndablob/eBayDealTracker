import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

import eBay_API, db, plot
from datetime import datetime
import pymysql.cursors
import logging

root = tk.Tk()


def search_query():
    logging.warning(f"Search button pressed at {datetime.utcnow()}")

    query = query_entry.get()

    if query == "":
        messagebox.showwarning("Warning", f"The search query can not be blank")
        logging.warning("Blank search query")
        return

    try:
        d = eBay_API.search(query)
    except KeyError:
        messagebox.showerror("Error", f"API KeyError")
        logging.error("API KeyError")
        return

    total_entries = int(d['searchResult']['_count'])
    if total_entries == 0:
        messagebox.showerror("Error", f"There are no entries for the given search query")
        logging.error("No entries for the given search query")
        return

    while True:
        entries = simpledialog.askinteger("Entries",
                                          f"Out of {total_entries} total entries, how many would you like to display?")

        if entries > total_entries or entries < 0:
            messagebox.showerror("Error", f"Invalid number of entries")
            logging.error("Invalid entries bound")
        else:
            break

    # pulling data from api
    for i in range(0, entries):
        timestamp = datetime.now()
        title = (d['searchResult']['item'][i]['title'])  # item title
        itemId = (d['searchResult']['item'][i]['itemId'])  # item ID
        price = (d['searchResult']['item'][i]['sellingStatus']['currentPrice']['value'])  # item price
        viewItemURL = (d['searchResult']['item'][i]['viewItemURL'])  # URL to view item
        # insert to treeview
        tree.insert('', tk.END, values=(timestamp, title, itemId, price, viewItemURL))


def send_all_db():
    for children in tree.get_children():
        r = tree.item(children)

        try:
            time = r['values'][0]
            title = r['values'][1]
            itemId = r['values'][2]
            price = r['values'][3]
            url = r['values'][4]
        except IndexError:
            messagebox.showerror("Error", f"No table rows selected")
            logging.error("No treeview row selected")
            return

        try:
            # Connect to the database
            connection = db.connect()

            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `filtered_product_info` (`timestamp`, `title`, `itemId`, `price`, `viewItemURL`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (time, title, itemId, price, url))

            # connection is not autocommit by default. So you must commit to save changes.
            connection.commit()
        except pymysql.err.OperationalError:
            logging.error("Database connection refused")
            messagebox.showerror("Error", "Database connection refused")
            return

    messagebox.showinfo("Info", f"Successfully stored all rows to the database")
    connection.close()


def clear_db_tables():
    ans = messagebox.askyesno("Confirmation", "Are you sure you want to clear the database table?")

    if ans:
        try:
            # Connect to the database
            connection = db.connect()

            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute("TRUNCATE TABLE filtered_product_info")

            # connection is not autocommit by default. So you must commit to save changes.
            connection.commit()

            messagebox.showinfo("Info", f"Successfully cleared database table")
        except pymysql.err.OperationalError:
            logging.error("Database connection refused")
            messagebox.showerror("Error", "Database connection refused")
            return
        connection.close()


def store_row():
    f = tree.item(tree.focus())

    try:
        time = f['values'][0]
        title = f['values'][1]
        itemId = f['values'][2]
        price = f['values'][3]
        url = f['values'][4]
    except IndexError:
        messagebox.showerror("Error", f"No table rows selected")
        logging.error("No treeview row selected")
        return

    try:
        # Connect to the database
        connection = db.connect()

        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `filtered_product_info` (`timestamp`, `title`, `itemId`, `price`, `viewItemURL`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (time, title, itemId, price, url))

        # connection is not autocommit by default. So you must commit to save changes.
        connection.commit()
    except pymysql.err.OperationalError:
        logging.error("Database connection refused")
        messagebox.showerror("Error", "Database connection refused")
        return

    messagebox.showinfo("Info", f"Successfully stored:\n{title} ")
    connection.close()


def show_price_graph():
    f = tree.item(tree.focus())

    try:
        itemId = f['values'][2]
    except IndexError:
        messagebox.showerror("Error", f"No table rows selected")
        logging.error("No treeview row selected")
        return

    t = []
    p = []
    for r in db.fetch():
        if r["itemId"] == itemId:
            p.append(r["price"])
            t.append(r["timestamp"].strftime("%m/%d/%Y  %H:%M:%S"))

    plot.plot(t, p)


# build ui
top_level = ttk.Frame(master=root)
header_label = ttk.Label(top_level)
header_label.configure(font='{Comic_Sans} 36 {bold}', text='eBay Deal Tracker')
header_label.grid(column=0, row=0)
input_frame = ttk.Frame(top_level)
query_label = ttk.Label(input_frame)
query_label.configure(font='{Comic_Sans} 16 {bold}', text='Search Query: ')
query_label.grid(column=0, sticky='e')
query_entry = ttk.Entry(input_frame)
query_entry.grid(column=1, row=0, sticky='e')
input_frame.configure(height='1024', width='576')
input_frame.grid(column=0, row=1)
button_frame = ttk.Frame(top_level)
button_search = ttk.Button(button_frame)
button_search.configure(default='normal', text='Search', command=search_query)
button_search.grid(column=0, row=0, sticky='e')
button_frame.configure(height='1024', width='576')
button_frame.grid(column=1, row=1, sticky='e')
top_level.configure(height='1024', width='576')
top_level.pack(side='top')


def popup(e):
    menu.tk_popup(e.x_root, e.y_root)


# tk.menu
menu = tk.Menu(root, tearoff=False)
menu.add_command(label="Store row to database", command=store_row)
menu.add_separator()
menu.add_command(label="Display historical pricing graph", command=show_price_graph)

root.bind("<Button-3>", popup)

# ttk.tree
# define tree columns
columns = ('time', 'title', 'itemId', 'price', 'viewItemURL')
tree = ttk.Treeview(root, columns=columns, show='headings')

# define headings
tree.heading('time', text='Time')
tree.heading('title', text='Item Name')
tree.heading('itemId', text='Item ID')
tree.heading('price', text='Price')
tree.heading('viewItemURL', text='Item URL')

# vertical scrollbar
scrollbar_y = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side=tk.RIGHT, fill='y')

scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(xscroll=scrollbar_x.set)
scrollbar_x.pack(side=tk.BOTTOM, fill='x')

# ttk.button for storing to db
db_button_store = ttk.Button(root)
db_button_store.configure(default='normal', text='Store Table to Database', command=send_all_db)

# ttk.button for clearing db table
db_button_clear = ttk.Button(root)
db_button_clear.configure(default='normal', text='Clear Database Table', command=clear_db_tables)

# display tree & button
tree.pack(fill='both')
db_button_store.pack(fill='both')
db_button_clear.pack(fill='both')

if __name__ == '__main__':
    root.title('eBay Deal Tracker')
    root.geometry('1024x576')
    root.mainloop()
