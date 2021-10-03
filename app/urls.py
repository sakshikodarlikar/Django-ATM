from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lang',views.lang,name='lang'),
    path('anothertrans',views.anothertrans,name='anothertrans'),
    path('options',views.options,name='options'),
    path('password',views.password,name='password'),
    path('successful',views.successful,name='successful'),
    path('wait',views.wait,name='wait'),
    path('withdraw',views.withdraw,name='withdraw'),
    path('transfer',views.transfer,name='transfer'),
    path('balenquiry',views.balenquiry,name='balenquiry'),
    path('changepin',views.changepin,name='changepin'),
]