from django.urls import path 
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('home/', views.home, name='home'),
    path('craft/', views.craft, name='craft'),
    path('show/', views.ShowOne, name='show'),
    path('order/', views.order, name='order'),
    path('logout/', views.logoutview, name='logout'),
    path('startover', views.startover, name='startover'),
    path('purchase', views.purchase, name='purchase'),  
    path('cancel/', views.cancel, name='cancel'),
    path('makefavorite/', views.makefavorite, name='makefavorite'),
    path('makeunfavorite/', views.makeunfavorite, name='makeunfavorite'),
    path('updateinfos/', views.updateinfos, name='updateinfos'),
    path('reorderfav/', views.reorderfav, name='reorderfav'),
    path('surpriseme/', views.surpriseme, name='surpriseme'),
]
