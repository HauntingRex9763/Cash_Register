import csv, os, datetime, pandas as pd

class Product:
    '''
    Methods:
    --------
    __init__(self, name=str, cost=float, quantity=float)
        WORDS
    
    __str__(self)
        WORDS

    __repr__(self)
        WORDS
    
    __eq__(self)
        WORDS
    
    __set_ID(inventory_reader)
        WORDS
    
    __zero_check(*args)
        WORDS

    delete(ID=int)
        WORDS
    
    get_inventory_list()
        WORDS
    
    transaction(cart = list, key = str)
        WORDS
    '''
    def __init__(self, name=str, cost=float, quantity=float):
        self.inventory_csv = open(f'{os.getcwd()}\inventory_csv.csv','a',newline='')
        self.sales_history_csv = open(f'{os.getcwd()}\sales_history_csv.csv','a',newline='')

        self.inventory_reader = open(f'{os.getcwd()}\inventory_csv.csv', "r", encoding="utf-8", errors="ignore")
        self.inventory_writer = csv.writer(self.inventory_csv)
        self.sales_writer = csv.writer(self.sales_history_csv)

        Product.__zero_check(cost, quantity)
        self._name = name
        self._cost = cost
        self._quantity = quantity
        self._ID = self.__set_ID(self.inventory_reader)
        self.inventory_writer.writerow([name, cost, quantity, self._ID])
    
    def __str__(self):
        return f'''
Product:
    Name:   {self._name}
    Cost:   {self._cost}
    Amount: {self._quantity}
    ID:     {self._ID}
        '''

    def __repr__(self):
        return  f'Product('\
                f'name = {self._name}, '\
                f'cost = {self._cost}, '\
                f'amount = {self._quantity})'

    def __eq__(self, other):
        return True if self._ID == other._ID else False
    
    @staticmethod
    def __set_ID(inventory_reader):     
        final_ID = int(inventory_reader.readlines()[-1].split(',')[-1]) 
        return final_ID + 1

    @staticmethod
    def __zero_check(*args):
        for arg in args:
            if arg < 0:
                raise Exception(f'Value Error:\n{arg} is less than 0, cannot pass negetive values')
    
    @staticmethod
    def delete(ID=int):
        product_list = []
        with open(f'{os.getcwd()}\inventory_csv.csv','r',newline='') as file:
            for product in file:
                if int(product.split(',')[-1]) != ID:
                    product_list.append(product)
        with open(f'{os.getcwd()}\inventory_csv.csv','w',newline='') as file:
            writer = csv.writer(file)
            for product in product_list:
                writer.writerow([product.split(',')[0], float(product.split(',')[1]), float(product.split(',')[2]), int(product.split(',')[3])])

    @staticmethod
    def get_inventory_list():
        products = []
        with open(f'{os.getcwd()}\inventory_csv.csv','r',newline='') as file:
            for product in file:
                products.append(product)
        return products

    @staticmethod
    def transaction(cart = list, key = str):

        #Product.__zero_check(quantity)
        pd_file = pd.read_csv(f'{os.getcwd()}\inventory_csv.csv', header = None)

        # Open files and create writers
        with open(f'{os.getcwd()}\inventory_csv.csv','w',newline='') as inventory_file:
            inventory_writer = csv.writer(inventory_file)
            with open(f'{os.getcwd()}\sales_history_csv.csv','a',newline='') as sales_file:
                sales_writer = csv.writer(sales_file)

                # Creates interaction labels
                if key == 'sold': sales_writer.writerow(['TRANSACTION', datetime.datetime.now()])
                elif key == 'stocked': sales_writer.writerow(['RESTOCK', datetime.datetime.now()])
                elif key == 'writeoff': sales_writer.writerow(['WRITEOFF', datetime.datetime.now()])

                # Creates a line for each item manipulated in an indent
                for product, count in zip(cart, range(0, len(cart)+1)): 
                    for i, row in zip(pd_file.values, range(0, len(pd_file.values) + 1)):
                        if row == int(pd_file.index[pd_file[3] == int(product[2])][0]):
                            
                            # Check if stocked, written off or bought, calls respective methods, and records the transaction
                            if key == 'stocked':
                                inventory_writer.writerow([i[0], i[1], i[2] + product[1], i[3]])
                                sales_writer.writerow(['    '+str(i[0]), i[1], product[1], round(i[1] * product[1], 2), pd_file.values[pd_file.index[pd_file[3] == int(product[2])]][0][2] + product[1]])

                            elif key == 'sold':
                                if pd_file.values[pd_file.index[pd_file[3] == int(product[2])]][0][2] - product[1] < 0:
                                    #SEND BAD STOCK NOTIFICATION HERE
                                    inventory_writer.writerow([i[0], i[1], 0, i[3]])
                                else:
                                    inventory_writer.writerow([i[0], i[1], i[2] - product[1], i[3]])
                                sales_writer.writerow(['    '+str(i[0]), i[1], product[1], round(i[1] * product[1], 2), pd_file.values[pd_file.index[pd_file[3] == int(product[2])]][0][2] - product[1]])

                            elif key == 'writeoff':
                                if pd_file.values[pd_file.index[pd_file[3] == int(product[2])]][0][2] - product[1] < 0:
                                    #SEND BAD STOCK NOTIFICATION HERE
                                    inventory_writer.writerow([i[0], i[1], 0, i[3]])
                                else:
                                    inventory_writer.writerow([i[0], i[1], i[2] - product[1], i[3]])
                                sales_writer.writerow(['    '+str(i[0]), i[1], product[1], round(i[1] * product[1], 2), pd_file.values[pd_file.index[pd_file[3] == int(product[2])]][0][2] - product[1]])

                        # Keeps unaltered items in the inventory csv
                        else:
                            if count == len(cart)-1: 
                                inventory_writer.writerow(i) 
                
                return round(product[1] * pd_file.values[pd_file.index[pd_file[3] == int(product[2])]][0][1], 2)

if '__main__' == __name__:
    pass