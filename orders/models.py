from django.db import models
from django.contrib.auth.models import User

CRUST = (
    # (value, label)
    ('Regular', 'Regular pizza'),
    ('Sicilian', 'Sicilian pizza'),
)

SIZE = (
    ('large', 'large'),
    ('small', 'small')
)

PIZ_FLAVORS = (
    ('cheese', 'cheese'),
    ('1', '1 topping'),
    ('2', '2 toppings'),
    ('3', '3 toppings'),
    ('special', 'special')
)


# Pizza models 
class PizzaMenu(models.Model):
    crust = models.CharField(max_length=13, choices=CRUST, default='RegularPizza')
    size = models.CharField(max_length=6, choices=SIZE, default='small')
    flavor = models.CharField(max_length=10, choices=PIZ_FLAVORS, default='2')
    price = models.FloatField(default=7.5)

    class Meta:
         constraints = [
            models.UniqueConstraint(fields=['crust', 'size', 'flavor'], name='unique_pizza')
        ]   
 
    def __str__(self):
        if self.flavor in '123':
            flavor = f'{self.flavor} toppings'
            if self.flavor == '1':
                flavor = flavor[:-1]
        else:
            flavor = self.flavor
        return f'{self.size.capitalize()} {self.crust} pizza with {flavor} / {self.price}$'


class Topping(models.Model):
    item = models.CharField(max_length=64, unique=True, blank=False)

    def __str__(self):
        return f'{self.item}'

class PizzaOrder(models.Model):
    # delete entry when menu is deleted
    menu = models.ForeignKey(PizzaMenu, on_delete=models.CASCADE, related_name='pizzaMenus')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pizzaCustomers')
    toppings = models.ManyToManyField(Topping, blank=True)
    ordered = models.BooleanField()
    finished = models.BooleanField()
    price = models.FloatField()

    def __str__(self):
        return f'{self.menu} by {self.customer.username} / status: ({self.ordered}, {self.finished})'


# Subs models
class SubsFlavor(models.Model):
    flavor = models.CharField(max_length=64, unique=True, blank=False)

    def __str__(self):
        return f'{self.flavor}'


class SubsMenu(models.Model):
    size = models.CharField(max_length=6, choices=SIZE, default='small')
    flavor = models.ForeignKey(SubsFlavor, on_delete=models.CASCADE) 
    price = models.FloatField(default=6.5)

    class Meta:
         constraints = [
            models.UniqueConstraint(fields=['size', 'flavor'], name='unique_subs')
        ]
    
    def __str__(self):
        return f'{self.size.capitalize()} sub with {self.flavor} / {self.price}$'


class SubsExtra(models.Model):
    item = models.CharField(max_length=64, default='ExtraCheese')
    size = models.CharField(max_length=6, choices=SIZE, default='small')
    price = models.FloatField(default=0.5)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'size'], name='unique_subsExtra')
        ]

    def __str__(self):
        return f'{self.item}'

        
class SubsOrder(models.Model):
    menu = models.ForeignKey(SubsMenu, on_delete=models.CASCADE, related_name='subsMenus', null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subsCustomers', null=True)
    extras = models.ManyToManyField(SubsExtra, blank=True)
    ordered = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    
    def __str__(self):
        return f'{self.menu} by {self.customer.username} / status: ({self.ordered}, {self.finished})'

