import csv, os, datetime, pandas as pd

class Product:
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
    def get_data(email):
        # Get a way to send both csvs to user
        pass

    @staticmethod
    def transaction(ID, quantity=float, key = str):

        Product.__zero_check(quantity)
        pd_file = pd.read_csv(f'{os.getcwd()}\inventory_csv.csv', header = None)

        # Updates inventory
        with open(f'{os.getcwd()}\inventory_csv.csv','w',newline='') as inventory_file:
            writer = csv.writer(inventory_file)
            for i, row in zip(pd_file.values, range(0, len(pd_file.values) + 1)):
                # Catches bought item by ID
                if row == int(pd_file.index[pd_file[3] == int(ID)][0]):
                    
                    # Check if stocked or bought, calls respective methods, and records the transaction
                    if key == 'stocked':
                        writer.writerow([i[0], i[1], i[2] + quantity, i[3]])

                        with open(f'{os.getcwd()}\sales_history_csv.csv','a',newline='') as sales_file:
                            writer = csv.writer(sales_file)    
                            writer.writerow(['RESTOCK',i[0], i[1], quantity, round(i[1] * quantity, 2), pd_file.values[pd_file.index[pd_file[3] == int(ID)]][0][2] - quantity, datetime.datetime.now()])

                        #return round(quantity * pd_file.values[pd_file.index[pd_file[3] == int(ID)]][0][1], 2)

                    elif key == 'sold':
                        writer.writerow([i[0], i[1], i[2] - quantity, i[3]])

                        with open(f'{os.getcwd()}\sales_history_csv.csv','a',newline='') as sales_file:
                            writer = csv.writer(sales_file)    
                            writer.writerow(['SOLD',i[0], i[1], quantity, round(i[1] * quantity, 2), pd_file.values[pd_file.index[pd_file[3] == int(ID)]][0][2] + quantity, datetime.datetime.now()])

                        return round(quantity * pd_file.values[pd_file.index[pd_file[3] == int(ID)]][0][1], 2)

                # If not bought item, keep same
                else:
                    writer.writerow([i[0], i[1], i[2], i[3]])
  
        
    
    def get_name(self):
        return self._name
    
    def get_cost(self):
        return self._cost

    def get_quantity(self):
        return self._quantity

    def get_ID(self):
        return self._ID

if '__main__' == __name__:
    print(Product.transaction(1100, 2, 'stock'))
