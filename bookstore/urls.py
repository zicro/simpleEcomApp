from django.urls import path

from bookstore import views
from django.contrib.auth import views as authViews
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('register/', views.register, name="register"),


    path('reset_password/', authViews.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', authViews.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', authViews.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]