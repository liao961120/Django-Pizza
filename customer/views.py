from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html', {'message': None})
    #context = {'user': request.user}
    return HttpResponseRedirect(reverse('orders:index'))


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']

    # login
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('customer:index'))

    # ask to login again
    return render(request, 'customer/login.html', {'message': 'Invalide credentials.'})


def logout_view(request):
    logout(request)
    return render(request, 'customer/login.html', {'message': 'Logged out.'})


def register(request):
    if request.method == 'GET':
        return render(request, 'customer/register.html', {'message': None})
    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
    except:
        return render(request, 'customer/register.html', {'message': 'Invalid.'})

    # Check Username exists
    if User.objects.filter(username=username).exists():
        context = {
            'message': f'`{username}` already registered.'
        }
        return render(request, 'customer/register.html', context)
    
    # Successful registered
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return HttpResponseRedirect(reverse('customer:index'))
