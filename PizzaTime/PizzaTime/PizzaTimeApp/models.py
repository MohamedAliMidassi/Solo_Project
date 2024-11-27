from django.db import models
from django.contrib.auth.models import User

#! Topping Model
class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#! Pizza Model
class Pizza(models.Model):
    SIZE_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
    CRUST_CHOICES = [('Thin', 'Thin Crust'), ('Thick', 'Thick Crust')]

    name = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    crust = models.CharField(max_length=5, choices=CRUST_CHOICES)
    toppings = models.ManyToManyField('Topping')

    def __str__(self):
        return f"{self.name} - {self.size} {self.crust}"

    def get_price(self):
        base_price = 0  
        if self.size == 'S':
            base_price += 2
        elif self.size == 'M':
            base_price += 4
        else:
            base_price += 6
        if self.crust == 'Thin':
            base_price += 1
        else:
            base_price += 3
        base_price += len(self.toppings.all()) * 2
        return base_price

#! Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, related_name='orders')
    is_completed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        self.total_price = sum(pizza.get_price() for pizza in self.pizzas.all())
        self.save()