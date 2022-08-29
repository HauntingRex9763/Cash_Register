class Cart:
    def __init__(self):
        self.cart = []

    def add(self, product, quantity, ID):
        self.cart.append([product, quantity, ID])
    
    def clear(self):
        self.cart = []
    
    def remove(self, in_ID):
        # Cycles through cart and maintains index of current item
        for item, index in zip(self.cart, range(0, len(self.cart) + 1)):

            # If item in iter == item to be poppped
            if int(item[2]) == int(in_ID):
                self.cart.pop(index)
                return True
                
        return False

    def get_total(self):
        total = 0
        for product in self.cart:
            total += round(float(product[0][1]) * float(product[1]), 2)
        return total

    def get(self):
        return self.cart