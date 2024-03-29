class Inventory_Management:
    def __init__(self, window):
        from os import getcwd; import pandas as pd
        self.window  = window
        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        pd_file = pd.read_csv(open(f'{getcwd()}\\totally_not_a_password.csv', 'r', encoding="utf-8", errors="ignore"))
        self.password = pd_file.values[0][0]
        print(self.password)

        tk.Label(self.window, text='Enter login password -> \nPress enter to continue').grid(row=0, column=0)
        self.entry = tk.Entry(self.window); self.entry.grid(row=0, column=1)

        self.window.bind('<Return>', lambda x: self.getter())
        self.window.title('Sign-In')
        self.window.geometry("1000x300")
        self.window.mainloop() 
        
    def getter(self):
        
        if self.entry.get() == self.password:
            Main_Page(self.window)
        else:
            # Clears window
            for widget in self.window.winfo_children():
                widget.destroy()
            tk.Label(self.window, text='Incorrect password, press enter to retry.').grid(row=0, column=0)
            self.window.bind('<Return>', lambda x: Inventory_Management(self.window))

class Add_Product_Window:
    '''
    Methods:
    --------
    __init__(self, window)
        WORDS
    
    add_product(self)
        WORDS
    '''
    def __init__(self, window):
        self.window = window
        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Decorates window
        self.window_dict = {} 
        tk.Label(self.window, text = "Enter Name ->").grid(row=0, column=0)
        self.e1 = tk.Entry(self.window); self.e1.grid(row=0, column=1)
        tk.Label(self.window, text = "Enter Cost ->").grid(row=1, column=0)
        self.e2 = tk.Entry(self.window); self.e2.grid(row=1, column=1)
        tk.Label(self.window, text = "Enter Quantity ->").grid(row=2, column=0)
        self.e3 = tk.Entry(self.window); self.e3.grid(row=2, column=1)
        for label, entry, i in zip(self.window_dict.keys(), self.window_dict.values(), range(0, len(self.window_dict))):
            label.grid(row = i, column = 0)
            entry.grid(row = i, column = 1)
        tk.Label(self.window, text = "Press Enter To Continue, or Q to return to product selection").grid(row = 3, column = 0)
        self.window.bind('<Return>', lambda x: self.add_product())
        self.window.title('Add Product')

    def add_product(self):
        Product(self.e1.get(), float(self.e2.get()), float(self.e3.get()))

        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        tk.Label(self.window, text = "Product added succesfully, press Q to return to the main page.").grid(row=0, column=0)
        
class Product_Window:
    def __init__(self, window, product, ID):
        self.window = window
        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        self.in_prod = product
        self.ID = ID   
        
        # Find product info
        for product_iter in Product.get_inventory_list():
            if int(product_iter.split(',')[-1][0:4]) == int(ID):
                self.product = product_iter.split(',') 

        # Decorate new window
        tk.Button(self.window, text = 'Writeoff', command = lambda: self.transaction('writeoff')).grid(row = 0, column = 0)
        tk.Button(self.window, text = 'Stocked', command = lambda: self.transaction('stocked')).grid(row = 1, column = 0)
        tk.Button(self.window, text = 'Delete', command = lambda: self.delete()).grid(row = 2, column = 0)
        tk.Label(self.window, text = "Press Q To Go Back To Main Page").grid(row = 3, column = 0)
        self.window.bind('q', lambda x: Main_Page(self.window))   
        self.window.title(self.product[0])
        self.window.geometry("1000x300")
        self.window.mainloop() 

    def transaction(self, key):
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
            # Gets entry, do this before window clear because deleting the widgets also deletes entry's data
            entry = float(self.entry.get())
            # Clears window
            for widget in self.window.winfo_children():
                widget.destroy()
            self.window.bind('<Return>', lambda x: Product_Window(self.window, self.in_prod, self.ID))
            
        except: 
            for widget in self.window.winfo_children():
                widget.destroy()
            tk.Label(self.window, text = "Quantity must be a number, press return to go back to re-enter the amount, or Q to return to the product selection page").grid(row=0, column=0)
            
        else:
           Product.transaction([[self.product, entry, self.ID]], self.key)
           tk.Label(self.window, text = f"Item added to cart\nPress return to go back to the product, or Q to return to the product selection page").grid(row=0, column=0)

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
        self.window = window
        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Decorates new window
        tk.Button(self.window, text = 'Add Product', command = lambda: Add_Product_Window(self.window)).grid(row=0, column=0)

        # Builds product disply in rows of ten
        for product, i in zip(Product.get_inventory_list(), range(0, len(Product.get_inventory_list()))):
            product = product.split(',')
            j = i // 10; i -= j * 10
            tk.Button(self.window, text = product[0], command = partial(Product_Window, self.window, product, int(product[-1][0:4]))).grid(row = j + 1, column = i)
        self.window.title('Belleisle Gardens Inventory Management')
        self.window.geometry("1000x300")
        self.window.mainloop()

if '__main__' == __name__:
    import tkinter as tk; from product import *; from functools import partial; from cart import *
    Inventory_Management(tk.Tk())