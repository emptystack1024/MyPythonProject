class Product:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price

    def quote(self,User):
        return self.price

class User:
    def __init__(self, name):
        self.name = name

    def inquiry(self, product):
        print(product.quote(product))
        return


x = User('x')
y = User('y')
a = Product('a',1,10)
b = Product('b',2,11)
c = Product('c',3,12)

x.inquiry(a)
x.inquiry(b)