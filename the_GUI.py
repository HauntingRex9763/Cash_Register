class Add_Product_Window:
    '''
    ***UNDER CONSTRUCTION - IGNORE ME***
    Methods:
    --------
    __init__(self, window)
        WORDS
    
    add_product(self)
        WORDS
    '''
    def __init__(self, window):
        # Delete old window
        window.destroy()

        # Creates new window
        self.window = tk.Tk()

        # Decorates window
        self.window_dict = {} 
        self.window_dict[tk.Label(self.window, text = "Enter Name ->")] = tk.Entry(self.window)
        self.window_dict[tk.Label(self.window, text = "Enter Cost ->")] = tk.Entry(self.window)
        self.window_dict[tk.Label(self.window, text = "Enter Quantity ->")] = tk.Entry(self.window)
        for label, entry, i in zip(self.window_dict.keys(), self.window_dict.values(), range(0, len(self.window_dict))):
            label.grid(row = i, column = 0)
            entry.grid(row = i, column = 1)
        tk.Label(self.window, text = "Press Enter To Continue, or Q to return to product selection").grid(row = 3, column = 0)
        self.window.bind('<Return>', lambda x: self.add_product())
        self.window.title('Add Product')
        self.window.geometry("300x300")
        self.window.mainloop()

    # Takes entrys and makes a new product object   
    def add_product(self):
        product = []
        for entry in self.window_dict.values():
            product.append(entry.get())
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.bind('<Return>',lambda x: Add_Product_Window(self.window))
        self.window.bind('q',lambda x: Main_Page(self.window))

        try:
            Product(product[0], float(product[1]), float(product[2]))
        except: 
            tk.Label(self.window, text = "Cost and Quantity must be a number, press return to go back to product page or 'Q' to go to home page").grid(row=0, column=0)
        else:
            tk.Label(self.window, text = "Product added, press return to add another product or 'Q' to go to home page").grid(row=0, column=0) 

class Product_Window:
    '''
    Methods:
    --------
    __init__
        Creates a new window, deletes the old one, and displays options to either buy, restock, or delete the selected object from Main_Page

    transaction(window, product, ID)
        clears the window, and makes entry for the quantity to be either stocked or sold depending on the selection from __INIT__
    
    getter(self)
        gets the entry from transaction, checks it, and tries it in Product.transaction

    delete(self)
        deletes the product from the inventory_csv.csv
    '''
    def __init__(self, window, product, ID):
        print(product, ID)
        self.in_prod = product
        self.ID = ID   
        
        # Find product info
        for product_iter in Product.get_inventory_list():
            if int(product_iter.split(',')[-1][0:4]) == int(ID):
                self.product = product_iter.split(',') 
        
        # Delete old window
        window.destroy()

        # Create new window
        self.window = tk.Tk()

        # Decorate new window
        tk.Button(self.window, text = 'Sold', command = lambda: self.transaction('sold')).grid(row = 0, column = 0)
        tk.Button(self.window, text = 'Stocked', command = lambda: self.transaction('stocked')).grid(row = 1, column = 0)
        tk.Button(self.window, text = 'Delete', command = lambda: self.delete()).grid(row = 2, column = 0)
        tk.Label(self.window, text = "Press Q To Go Back To Main Page").grid(row = 3, column = 0)
        self.window.bind('q', lambda x: Main_Page(self.window))   
        self.window.title(self.product[0])
        self.window.geometry("1000x300")
        self.window.mainloop() 
 
    def transaction(self, key = str):
        self.key = key

        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Re-decorates window
        tk.Label(self.window, text = "Enter Quantity ->").grid(row = 0, column = 0)
        self.entry = tk.Entry(self.window); self.entry.grid(row = 0, column = 1)
        tk.Label(self.window, text = "Press Enter To Continue\nPress Q to return to product page").grid(row = 1, column = 0)
        self.window.bind('<Return>', lambda x: self.getter())

    def getter(self):       
        # Gets quantity entry and checks if the entry is acceptable as float
        try:
            for widget in self.window.winfo_children():
                widget.destroy()
            self.window.bind('<Return>', lambda x: Product_Window(self.window, self.in_prod, self.ID))
            entry = float(self.entry.get())
            
        except: 
            tk.Label(self.window, text = "Quantity must be a number, press return to go back to re-enter the amount, or Q to return to the product selection page").grid(row=0, column=0)
            
        else:
            tk.Label(self.window, text = f"Due change for {entry} {self.product[0]} bought is: {float(Product.transaction(self.ID, float(entry), self.key))}\nPress return to go back to the product, or Q to return to the product selection page").grid(row=0, column=0)

    def delete(self):
        # Clears window
        for widget in self.window.winfo_children():
                widget.destroy()

        # Re-decorates window
        self.window.bind('<Return>', lambda: Product_Window(self.window, self.in_prod, self.ID))
        self.window.bind('q', lambda x: Main_Page(self.window))

        # Delete process
        try:
            Product.delete(self.ID)

        except: 
            tk.Label(self.window, text = "ID has to be an integer, press return to go back to delete page or 'Q' to go to home page").grid(row=0, column=0)
        
        else:
            tk.Label(self.window, text = "Delete complete, press return to go back to delete again page or 'Q' to go to home page").grid(row=0, column=0)

class Main_Page:
    '''
    __init__
        cycles through inventory_csv.csv and posts a button representing each item in the store's inventory 
    '''
    def __init__(self, window):
        # Delete old window
        window.destroy()

        # Create new window
        self.window = tk.Tk()

        # Decorates new window
        tk.Button(self.window, text = 'Add Product', command = lambda: Add_Product_Window(self.window)).grid(row=0, column=0)
        # Builds product disply in rows of ten
        for product, i in zip(Product.get_inventory_list(), range(0, len(Product.get_inventory_list()))):
            product = product.split(',')
            j = i // 10; i -= j * 10
            tk.Button(self.window, text = product[0], command = partial(Product_Window, self.window, product, int(product[-1][0:4]))).grid(row = j + 1, column = i)
        self.window.title('Belleisle Gardens Cash Register')
        self.window.geometry("1000x300")
        self.window.mainloop()

import tkinter as tk; from product import *; from functools import partial
Main_Page(tk.Tk())