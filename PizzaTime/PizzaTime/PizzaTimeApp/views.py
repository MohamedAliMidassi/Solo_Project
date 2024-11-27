from django.shortcuts import render, redirect
from .forms import RegistrationForm,PizzaForm
from .models import Pizza,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required

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
def login_view(request):
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




#! Logout view
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')




#! Home view
@login_required
def home(request):
    return render(request, 'home.html')



#! Order view
@login_required
def order(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()  
    if order:
        order.calculate_total_price()  
    return render(request, 'order.html', {'order': order})



#! Craft a pizza view
@login_required
def craft(request):
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
    
    return render(request, 'craft.html', {'form': form})



#! Show information view
@login_required
def ShowOne(request):
    return render(request,'showorder.html')
