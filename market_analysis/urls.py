from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index,name='index'),
    path('', views.loginn,name='login'),
    path('data_view', views.data_view,name='data_view'),
   
]