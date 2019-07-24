from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.shoppingChart, name='shoppingChart'),
    path('showMenu', views.showMenu, name='showMenu'),
    path('add2chart', views.add2chart, name='add2chart')
]
