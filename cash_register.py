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
        self.window = window

        # Clears window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Find product info
        for product_iter in Product.get_inventory_list():
            if int(product_iter.split(',')[3][0:4]) == int(ID):
                self.product = product_iter.split(',') 

        # Re-decorates window
        tk.Label(self.window, text = "Enter Quantity ->").grid(row = 0, column = 0)
        self.entry = tk.Entry(self.window); self.entry.grid(row = 0, column = 1)
        tk.Label(self.window, text = "Press Enter To Continue\nPress Q to return to product page").grid(row = 1, column = 0)
        self.window.bind('<Return>', lambda x: self.getter())
        
        self.window.bind('q', lambda x: Main_Page(self.window))   
        self.window.title(self.product[0])
    

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
            if entry < 0:
                tk.Label(self.window, text = "Quantity must be a posotive number, press return to go back to re-enter the amount, or Q to return to the product selection page").grid(row=0, column=0)
            else:
                shopping_cart.add(self.product, entry, self.ID)
                tk.Label(self.window, text = f"Item added to cart\nPress return to go back to the product, or Q to return to the product selection page").grid(row=0, column=0)

#*** Make func in product that checks if the subtraction results in a negetive quantity than return false and cancel the operation and the false will run the failsave func in the Cart_Window class 
class Cart_Window:
    '''
    Methods:
    --------
    __init__(window)
        Clears window and builds a cart management dispay
    
    failsave()
        Called when the action removes more product than is in stock to prevent a negetive inventory
    
    get_change()
        Is called with the total passed as a paramater to break down into change displayed on the window after the purchase goes through
    
    view()
        Displays the product, # bought x cost in a column when clicked for each item in cart with an option to remove each singular itenm in the cart
    
    remove_func()
        Called when a item is removed while in view mode of the cart

    clear()
        Deletes the entire cart
    
    buy()
        Calls product.Product.transaction and displays the results 

    
    '''
    def __init__(self, window):
        self.window = window
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()

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
        self.window = window
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Decorates new window
        tk.Button(self.window, text = 'Cart', command = lambda: Cart_Window(self.window)).grid(row=0, column=0)
        # Builds product disply in rows of ten
        for product, i in zip(Product.get_inventory_list(), range(0, len(Product.get_inventory_list()))):
            product = product.split(',')
            j = i // 10; i -= j * 10
            tk.Button(self.window, text = product[0], command = partial(Product_Window, self.window, product, int(product[3][0:4]))).grid(row = j + 1, column = i)
        self.window.title('Belleisle Gardens Cash Register')
        self.window.geometry("1000x300")
        self.window.mainloop()

if '__main__' == __name__:
    import tkinter as tk; from product import *; from functools import partial; from cart import *
    shopping_cart = Cart()
    Main_Page(tk.Tk())
