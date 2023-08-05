from django.forms import ModelForm
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        #fields = "__all__"
        fields = ['username', 'email', 'password1', 'password2']