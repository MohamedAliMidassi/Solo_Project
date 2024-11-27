from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('order/', views.order, name='order'),
    path('craft/',views.craft,name='craft'),
    path('show/',views.ShowOne,name='show')
]
