from django.forms import ModelForm
from .models import*
from .models import Producto
from .models import Categoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1','password2']


class Producto_Form(ModelForm):
    class Meta:
        model =   Producto
        fields =  ['codigo', 'nombre', 'precio', 'fecha_vencimiento' ,'especificaciones', 'peso', 'categoria','foto', 'foto1', 'foto2']      

class Categoria_Form(ModelForm):
    class Meta:
        model =   Categoria
        fields =  [ 'codigo','nombre' ,'especificaciones'] 