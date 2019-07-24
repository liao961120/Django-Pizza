from django.contrib import admin
from .models import PizzaMenu, PizzaOrder, Topping, SubsMenu, SubsExtra, SubsFlavor, SubsOrder

# Register your models here.
admin.site.register(PizzaMenu)
admin.site.register(PizzaOrder)
admin.site.register(Topping)
admin.site.register(SubsFlavor)
admin.site.register(SubsMenu)
admin.site.register(SubsExtra)
admin.site.register(SubsOrder)