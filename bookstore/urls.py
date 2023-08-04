from django.urls import path

from bookstore import views

urlpatterns = [
    path('', views.home, name="home"),
    path('books/', views.books, name="books"),
    #path('customer/', views.customer),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('profile/', views.profile, name="profile"),
    path('create/', views.create, name="create"),
]