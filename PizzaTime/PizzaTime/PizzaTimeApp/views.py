from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,PizzaForm
from .models import Pizza,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
import random


#! User registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
                return render(request, 'register.html', {'form': form})  
            else:
                
                user = User.objects.create_user(
                    username=email,  
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=email,
                    password=form.cleaned_data['password']
                )

                
                login(request, user)
                return redirect('home')  
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})





#! Login view
def loginview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    
    return render(request, 'login.html')








#! Home view
@login_required
def home(request):
    order_count = Order.objects.count()
    return render(request, 'home.html',{'order_count': order_count})

@login_required
def reorderfav(request):
    if request.method == 'POST':
        favorite_order = Order.objects.filter(user=request.user, favorite=True).first()
        if not favorite_order:
            return redirect('home') 
        new_order = Order.objects.create(user=request.user, is_completed=False)
        for pizza in favorite_order.pizzas.all():
            new_order.pizzas.add(pizza)
        new_order.calculate_total_price()
        return redirect('order')
    return redirect('home')

@login_required
def surpriseme(request):
    if request.method == 'POST':
        availablepizzas = Pizza.objects.all()
        if not availablepizzas:
            return redirect('craft')
        random_pizza = random.choice(availablepizzas)
        new_order = Order.objects.create(user=request.user, is_completed=False)
        new_order.pizzas.add(random_pizza)
        new_order.calculate_total_price()
        return redirect('order')

    return redirect('home')





#! Craft a pizza view
@login_required
def craft(request):
    order_count = Order.objects.count()
    order_count = Order.objects.count()
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.save()
            form.save_m2m()
            order, created = Order.objects.get_or_create(
                user=request.user,
                is_completed=False
            )
            order.pizzas.add(pizza)
            order.calculate_total_price()
            order.save()
            return redirect('order')  
    else:
        form = PizzaForm()
    
    return render(request, 'craft.html', {'form': form,'order_count': order_count})

#! Show information view
@login_required
def ShowOne(request):
    order_count = Order.objects.count()
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = Order.objects.get(id=order_id, user=request.user)
            order.favorite = not order.favorite  
            order.save()
    user_infos = request.user
    orders = Order.objects.filter(user=user_infos).order_by('-created_at')
    return render(request, 'showorders.html', {'user_infos': user_infos, 'orders': orders, 'order_count': order_count})

@login_required
def updateinfos(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('show') 
    return redirect('show')

@login_required
def makefavorite(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id, user=request.user)
            order.favorite = True  
            order.save()
            return redirect('show')  
    return redirect('show')
@login_required
def makeunfavorite(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id, user=request.user)
            order.favorite = False  
            order.save()
            return redirect('show')  
    return redirect('show')


#! Order view
@login_required
def order(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()  
    if order:
        order.calculate_total_price()  
    return render(request, 'order.html', {'order': order})

@login_required
def startover(request):
    if request.method == 'POST':
        order = Order.objects.filter(user=request.user, is_completed=False).first()
        if order:
            order.delete()
        return redirect('craft') 
    return redirect('order')

@login_required
def purchase(request):
    if request.method == 'POST':
        order = Order.objects.filter(user=request.user, is_completed=False).first()
        if order:
            order.is_completed = True 
            order.save()
            return redirect('home') 
        else:
            return redirect('craft') 
    return redirect('order') 

@login_required
def cancel(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    if order:
        order.delete()
    return redirect('home')





#! Logout view
@login_required
def logoutview(request):  
    if request.user.is_authenticated:
        logout(request) 
    return redirect('login')






