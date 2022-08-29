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
    __init__(window, product, ID)
        Creates a new window, deletes the old one, and displays options to either buy, restock, or delete the selected object from Main_Page

    transaction(window, product, ID)
        clears the window, and makes entry for the quantity to be either stocked or sold depending on the selection from __INIT__
    
    getter(self)
        gets the entry from transaction, checks it, and tries it in Product.transaction

    delete(self)
        deletes the product from the inventory_csv.csv
    '''
    def __init__(self, window, product, ID):
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
            shopping_cart.add(self.product, entry, self.ID)
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

class Cart_Window:
    '''
    Methods:
    --------
    __init__(window)
        WORDS
    
    view()
        WORDS
    
    clear()
        WORDS
    
    buy()
        WORDS
    '''
    def __init__(self, window):
        # Delete old window
        window.destroy()

        # Create new window
        self.window = tk.Tk()

        # Decorate new window
        tk.Button(self.window, text = 'View', command = lambda: self.view()).grid(row = 0, column = 0)
        tk.Button(self.window, text = 'Clear', command = lambda: self.clear()).grid(row = 1, column = 0)
        tk.Button(self.window, text = 'Buy', command = lambda: self.buy()).grid(row = 2, column = 0)
        tk.Label(self.window, text = "Press Q To Go Back To Main Page").grid(row = 3, column = 0)
        self.window.bind('q', lambda x: Main_Page(self.window))   
        self.window.title('Cart')
        self.window.geometry("1000x300")
        self.window.mainloop() 
    
    @staticmethod
    def get_change(total = float):
        in_fifty = total // 50
        in_twenty = round(total - in_fifty * 50, 2) // 20; total -= in_fifty * 50
        in_ten = round(total - in_twenty * 20, 2) // 10; total -= in_twenty * 20
        in_five = round(total - in_ten * 10, 2) // 5; total -= in_ten * 10
        in_tooney = round(total - in_five * 5, 2) // 2; total -= in_five * 5
        in_looney = round(total - in_tooney * 2, 2) // 1; total -= in_tooney * 2
        in_quarter = round(total - in_looney * 1, 2) // 0.25; total -= in_looney * 1
        in_dime = round(total - in_quarter * 0.25, 2) // 0.10; total -= in_quarter * 0.25
        in_nickel = round(total - in_dime * 0.10, 2) // 0.5
        return [in_fifty, in_twenty, in_ten, in_five, in_tooney, in_looney, in_quarter, in_dime, in_nickel]    

    def view(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Decorate window
        for product, index in zip(shopping_cart.get(), range(0, len(shopping_cart.get()))):
            tk.Label(self.window, text = f'{product[0][0]}: {product[1]}').grid(row = index, column = 0)
            tk.Button(self.window, text = 'Remove', command = partial(self.remove_func, product[0][3])).grid(row = index, column = 1)
            
        tk.Label(self.window, text = "Press Q To Go Back To Main Page").grid(row = len(shopping_cart.get()), column = 0)

    def remove_func(self, product_ID):
        # Two funcs need called on button, so this acts as a junction
        shopping_cart.remove(product_ID)
        self.view()

    def clear(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Clears the shopping_cart
        shopping_cart.clear()
        
        # Decorate window
        tk.Label(self.window, text = "Cart cleared\nPress Q To Go Back To Main Page").grid(row = 3, column = 0)

    def buy(self):
        change_total = self.get_change(shopping_cart.get_total())
        Product.transaction(shopping_cart.get(), 'sold')

        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Decorate window
        tk.Label(self.window, text = "Cost total for the purchase of").grid(row=0, column=0)
        row_len = 0
        for product, index in zip(shopping_cart.get(), range(1, len(shopping_cart.get())+1)):
            row_len = index +1
            tk.Label(self.window, text = f'{product[0][0]}: {product[1]} x {product[0][1]}$').grid(row = index, column = 0)
        tk.Label(self.window, text = f"Comes to {shopping_cart.get_total()}").grid(row = row_len+1, column=0)
        tk.Label(self.window, text = f"Change will be {change_total[0]} fiftys, {change_total[1]} twentys, {change_total[2]} tens, {change_total[3]} fives, {change_total[4]} tooneys, {change_total[5]} looneys, {change_total[6]} quarters, {change_total[7]} dimes, {change_total[8]} nickels,").grid(row=row_len+2, column=0)
        tk.Label(self.window, text = "Press return to go back to the product, or Q to return to the product selection page").grid(row=row_len+3, column=0)
        shopping_cart.clear()

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
        tk.Button(self.window, text = 'Cart', command = lambda: Cart_Window(self.window)).grid(row=0, column=1)
        # Builds product disply in rows of ten
        for product, i in zip(Product.get_inventory_list(), range(0, len(Product.get_inventory_list()))):
            product = product.split(',')
            j = i // 10; i -= j * 10
            tk.Button(self.window, text = product[0], command = partial(Product_Window, self.window, product, int(product[-1][0:4]))).grid(row = j + 1, column = i)
        self.window.title('Belleisle Gardens Cash Register')
        self.window.geometry("1000x300")
        self.window.mainloop()


import tkinter as tk; from product import *; from functools import partial; from cart import *
shopping_cart = Cart()
Main_Page(tk.Tk())
