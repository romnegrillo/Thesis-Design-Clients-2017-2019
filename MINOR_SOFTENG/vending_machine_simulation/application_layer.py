import string

class VendingMachine:

    def __init__(self,item_name=None,quantity=None,price_per_item=None):
        self.item_name=item_name
        self.quantity=quantity
        self.price_per_item=price_per_item

    def isItemNameValid(self,item_name):

        if not item_name or item_name.isspace():
            return False
        
        flag=True

        for item in item_name:
            if item not in string.punctuation:
                continue
            else:
                flag=False
                break
            
        return flag

    def isQuantityValid(self,quantity):
        
        try:
            quantity=int(quantity)
            return True
        except:
            return False

    def isPricePerItemValid(self,price_per_item):
        
        try:
            price_per_item=int(price_per_item)
            return True
        except:
            return False

    def isMoneyValid(self,price_per_item):
        validMoney=[20,50,100]
        try:
            price_per_item=int(price_per_item)
            if price_per_item in validMoney:
                return True
        except:
            return False

        return False
