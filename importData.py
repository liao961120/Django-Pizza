from orders.models import Topping, PizzaMenu, PizzaOrder, SubsFlavor, SubsExtra, SubsMenu
import itertools

# Deal with scoping problems in Django shell, see https://bit.ly/2Z3FwcV
globals().update(locals())

TOPPINGS = (
    'Pepperoni',
    'Sausage',
    'Mushrooms',
    'Onions',
    'Ham',
    'Canadian Bacon',
    'Pineapple',
    'Eggplant',
    'Tomato & Basil',
    'Green Peppers',
    'Hamburger',
    'Spinach',
    'Artichoke',
    'Buffalo Chicken',
    'Barbecue Chicken',
    'Anchovies',
    'Black Olives',
    'Fresh Garlic',
    'Zucchini',
)

PIZZA_PRICES = (
    ('cheese', '12.20', '17.45', '23.45', '37.70'),
    ('1', '13.20', '19.45', '25.45', '39.70'),
    ('2', '14.70', '21.45', '27.45', '41.70'),
    ('3', '15.70', '23.45', '28.45', '43.70'),
    ('special', '17.25', '25.45', '29.45', '44.70'),
)

SUBS_PRICES = (
    ('Cheese', '6.50', '7.95'),
    ('Italian', '6.50', '7.95'),
    ('Ham & Cheese', '6.50', '7.95'),
    ('Meatball', '6.50', '7.95'),
    ('Tuna', '6.50', '7.95'),
    ('Turkey', '7.50', '8.50'),
    ('Chicken Parmigiana', '7.50', '8.50'),
    ('Eggplant Parmigiana', '6.50', '7.95'),
    ('Steak', '6.50', '7.95'),
    ('Steak & Cheese', '6.95', '8.50'),
    ('Sausage & Peppers & Onions', 'null', '8.50'),
    ('Hamburger', '4.60', '6.95'),
    ('Cheeseburger', '5.10', '7.45'),
    ('Fried Chicken', '6.95', '8.50'),
    ('Veggie', '6.95', '8.50'),
)

SUBS_EXTRA = (
    ('Mushrooms', '0.50', '0.50'),
    ('GreenPeppers', '0.50', '0.50'),
    ('Onions', '0.50', '0.50'),
    ('ExtraCheese', '0.50', '0.50'),
)


# Add Pizza menu
def addPizzaMenu():
    global PIZZA_PRICES
    for tup in PIZZA_PRICES:
        for j, (crust, size) in enumerate(itertools.product(['Regular', 'Sicilian'], ['small', 'large'])):
            flavor = tup[0]
            price = float(tup[j+1])
            
            # Save to database
            pizza = PizzaMenu(crust=crust, size=size, flavor=flavor, price=price)
            pizza.save()

# Add Topping menu
def addToppingMenu():
    global TOPPINGS
    for item in TOPPINGS:
        t = Topping(item=item)
        t.save()

# Add Subs flavors
def addSubsFlavor_Menu():
    global SUBS_PRICES

    flv = ''
    for tup in SUBS_PRICES:
        for j, size in enumerate(['small', 'large']):
            # update flavor table
            if tup[0] != flv:
                flv = tup[0]
                flavor = SubsFlavor(flavor=flv)
                flavor.save()
            
            # deal with null price
            try:
                price = float(tup[j+1])
            except:
                continue 
            
            # update menu table
            sub = SubsMenu(size=size, flavor=flavor, price=price)
            sub.save()

# Add SubsExtra
def addSubsExtra():
    global SUBS_EXTRA
    for tup in SUBS_EXTRA:
        for j, size in enumerate(['small', 'large']):
            item = tup[0]
            price = float(tup[j+1])

            extra = SubsExtra(item=item, size=size, price=price)
            extra.save()


## Main function
addPizzaMenu()
addToppingMenu()
addSubsFlavor_Menu()
addSubsExtra()
