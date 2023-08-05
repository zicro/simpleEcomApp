from django.urls import path

from bookstore import views

urlpatterns = [
    path('', views.home, name="home"),
    path('books/', views.books, name="books"),
    #path('customer/', views.customer),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('profile/', views.profile, name="profile"),
    path('create/', views.create, name="create"),
    path('creates/<str:pk>', views.creates, name="creates"),
    path('update/<str:pk>', views.update, name="update"),
    path('delete/<str:pk>', views.delete, name="delete"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),

]