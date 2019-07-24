from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.apps import apps
import json
from .models import PizzaOrder, PizzaMenu, SubsOrder, SubsMenu

MODELS = {
    'PizzaMenu': (PizzaMenu, PizzaOrder),
    'SubsMenu': (SubsMenu, SubsOrder),
}

    
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('customer:index'))
    return HttpResponseRedirect(reverse('orders:shoppingChart')) 


def shoppingChart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('customer:index'))

    models = apps.get_models()
    menuTypes = [m for m in models if m.__name__.endswith('Menu')]
    menuItems = menuTypes[0].objects.all()
    
    context = {
        'message': request.user,
        'menuType': [(m.__name__, m.__name__[:-4]) for m in menuTypes],
    }
    return render(request, 'orders/menu.html', context)


def showMenu(request):
    if not request.is_ajax: return 

    # query menu based on Ajax POST request
    menuType_name = request.POST['menu-type']
    menuType = apps.get_model(model_name=menuType_name, app_label='orders')
    menuItems = menuType.objects.all()

    # write to dict
    items_array = []
    for item in menuItems:
        d = {
            'type': menuType_name,
            'id': item.id, 
            'item_str': str(item)
            }
        items_array.append(d)
    
    return JsonResponse(items_array, safe=False)

def add2chart(request):
    if not request.is_ajax: return {'success': False}
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('customer:index'))
    
    items = request.POST['items']  
    items = json.loads(items)  # an array

    # Create orders in xxxxOrders
    itemnum = 0
    for item in items:
        MenuModel = MODELS[item['menuType']][0]
        OrderModel = MODELS[item['menuType']][1]
        
        menu = MenuModel.objects.get(pk=int(item['id']))
        customer = request.user
        ordered = False
        finished = False
        price = menu.price

        for i in range(int(item['num'])):
            print(menu)
            order = OrderModel(menu=menu, customer=customer, ordered=ordered, finished=finished, price=price)
            print(order)
            order.save()
            itemnum += 1

    '''
    {'menuType': 'SubsMenu', 'id': '32', 'num': '1'}
    '''

    return JsonResponse({'success': True, 'itemnum': itemnum})