from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def  __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock =  models.IntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['price']

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Not Paid')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def  __str__(self):
        return f"Order{self.id+1}"




