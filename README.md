# Cash_Register

It's a cash

Cash register application, records products in inventory_csv.csv via NAME,COST,INVENTORY,ID
records sales history in sales_history_csv.csv TRANSACTION_TYPE,NAME,SINGLE_UNIT_COST,QUANTITY,TOTAL COST,REMAINING_STOCK,TIMESTAMP
product.py contains a variety of methods used to manipulate the CSVs according to the_GUI's commands
the_GUI.py is a file which contains the frontend for the application and sends requests to product.py
