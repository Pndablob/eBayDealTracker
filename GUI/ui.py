import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

import eBay_API
from datetime import datetime
import pymysql.cursors
import logging


class EbaydealtracketApp:
    def __init__(self, master=None):
        # build ui
        self.top_level = ttk.Frame(master)
        self.header_label = ttk.Label(self.top_level)
        self.header_label.configure(font='{Arial} 16 {bold}', text='eBay Deal Tracker')
        self.header_label.grid(column=0, row=0)
        self.input_frame = ttk.Frame(self.top_level)
        self.query_label = ttk.Label(self.input_frame)
        self.query_label.configure(text='Search Query:')
        self.query_label.grid(column=0, sticky='e')
        self.query_entry = ttk.Entry(self.input_frame)
        self.query_entry.grid(column=1, row=0, sticky='e')
        self.input_frame.configure(height='1024', width='576')
        self.input_frame.grid(column=0, row=1)
        self.button_frame = ttk.Frame(self.top_level)
        self.button_search = ttk.Button(self.button_frame)
        self.button_search.configure(default='normal', text='Search', command=self.on_button)
        self.button_search.grid(column=0, row=0, sticky='e')
        self.button_frame.configure(height='1024', width='576')
        self.button_frame.grid(column=0, row=3, sticky='e')
        self.top_level.configure(height='1024', width='576')
        self.top_level.pack(side='top')

        # Main widget
        self.mainwindow = self.top_level

    def run(self):
        self.mainwindow.mainloop()

    def on_button(self):
        logging.warning(f"Search button pressed at {datetime.utcnow()}")

        query = self.query_entry.get()

        if query == "":
            messagebox.showwarning("Warning", f"The search query can not be blank")
            logging.warning("Blank search query")
            return

        try:
            d = eBay_API.search(query)
            print(d)
        except KeyError:
            messagebox.showerror("Error", f"API KeyError")
            logging.error("API KeyError")
            return

        total_entries = int(d['searchResult']['_count'])
        if total_entries == 0:
            messagebox.showerror("Error", f"There are no entries for the given search query")
            logging.error("No entries for the given search query")
            return

        entries = simpledialog.askinteger("Entries", f"Out of {total_entries} total entries, how many would you like to display?")

        # pulling data from api
        attributes = []
        for i in range(0, entries):
            timestamp = datetime.utcnow()
            title = (d['searchResult']['item'][i]['title'])  # item title
            itemId = (d['searchResult']['item'][i]['itemId'])  # item ID
            price = (d['searchResult']['item'][i]['sellingStatus']['currentPrice']['value'])  # item price
            viewItemURL = (d['searchResult']['item'][i]['viewItemURL'])  # URL to view item

            attributes.append((timestamp, title, itemId, price, viewItemURL))

            try:
                # Connect to the database
                connection = pymysql.connect(host='localhost',
                                             user='',
                                             password='',
                                             database='product_info',
                                             cursorclass=pymysql.cursors.DictCursor)
                with connection:
                    with connection.cursor() as cursor:
                        # Create a new record
                        sql = "INSERT INTO `filtered_product_info` (`timestamp`, `title`, `itemId`, `price`, `viewItemURL`) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (timestamp, title, itemId, price, viewItemURL))
                    # connection is not autocommit by default. So you must commit to save changes.
                    connection.commit()
            except ConnectionRefusedError:
                logging.error("Database connection refused")

        # ttk.tree
        # define columns
        columns = ('time', 'title', 'itemId', 'price', 'viewItemURL')
        tree = ttk.Treeview(root, columns=columns, show='headings')
        # define headings
        tree.heading('time', text='Time')
        tree.heading('title', text='Item Name')
        tree.heading('itemId', text='Item ID')
        tree.heading('price', text='Price')
        tree.heading('viewItemURL', text='Item URL')

        # add data to treeview
        for attributes in attributes:
            tree.insert('', tk.END, values=attributes)

        # vertical scrollbar
        scrollbar_y = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill='y')

        scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill='x')

        # display tree
        tree.pack(fill='both')
        root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('eBay Deal Tracker')
    root.geometry('1024x576')
    app = EbaydealtracketApp(root)
    app.run()
