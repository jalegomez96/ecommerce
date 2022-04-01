from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse,Http404
from django.core.paginator import Paginator
from .models import  *
from .forms import CreateUserForm
from .forms import Producto_Form
from .forms import Categoria_Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import generic





def store(request):     
     # busquedad = request.GET.get("buscar") 
     producto =  Producto.objects.all().order_by("-id")
     # categorias : Categoria.objects.all()
     
     # imagenes = Imagen.objects.filter( # )  
     
     # data = {'producto' : producto}
     page =request.GET.get('page',1)
     try:
          paginator =Paginator(producto,9)
          producto = paginator.page(page)
     except:
          raise Http404

     
     return render(request, 'store/store.html',
     {

          'categorias' : Categoria.objects.all(),
          'productos_top3' : producto[:9],
          'producto' : producto[0:10000],
          'paginator' : paginator

     })

def cart(request):
     categorias = Categoria.objects.all()
     usuario = User.objects.get(username=request.user)
     productos = Carrito.objects.get(usuario=usuario.id).items.all()
     carrito = Carrito.objects.get(usuario=usuario.id)
  
     

     nuevo_precio_Carrito = 0
     for item in carrito.items.all():
          nuevo_precio_Carrito += item.producto.precio
          carrito.total = nuevo_precio_Carrito
          carrito.save()
     data = {'items_carrito' : productos,'usuario' : usuario, 'categorias' : categorias} 
     return render(request, 'store/cart.html',data)



def agregar_item(request,id):

     usuario = User.objects.get(username=request.user)
     producto = Producto.objects.get(id=id)

     try:
          carrito= Carrito.objects.get(usuario=usuario.id, estado='activo')
     except:

          carrito = Carrito()
          carrito.usuario = usuario 
          
          
          carrito.total = 0
          carrito.estado ='activo'
          carrito.save()#commit=False)
     
     # aqui le echamos un product

     item_carrito = Carrito_item()
     #item_carrito.save(commit=False)
     item_carrito.carrito = carrito
     item_carrito.producto = producto 
     item_carrito.save()
     
     carrito.total = carrito.total + item_carrito.subtotal +item_carrito.cantidad
     carrito.save()
     # messages.success(request, f"El producto {producto.nombre} fue agregado al carrito")
     return redirect('/')

#class IncreaseCantidadView(generic.View)
def IncreaseCantidad(request, id):
     item_carrito = get_object_or_404(Carrito_item, id=id)
     item_carrito.cantidad +=1
     item_carrito.save()
     return redirect("cart")




def DecreaseCantidad(request, id):
     item_carrito = get_object_or_404(Carrito_item, id=id)
     if item_carrito.cantidad <=1:
          item_carrito.delete()
     else:   
          item_carrito.cantidad -=1
          item_carrito.save()
     return redirect("cart")






     












def eliminar_carrito(request,id):
     eliminarCar =  Carrito_item.objects.get(id=id)
     carrito = eliminarCar.carrito
     nuvo_precio_Carrito = 0 - eliminarCar.producto.precio
     for item in carrito.items.all():
          nuvo_precio_Carrito += item.producto.precio


     carrito.total = nuvo_precio_Carrito
     eliminarCar.delete()
     carrito.save()
     return redirect('cart')














def checkout(request):
     categorias = Categoria.objects.all()
     usuario = User.objects.get(username=request.user)
     productos = Carrito.objects.get(usuario=usuario.id).items.all()
     carrito = Carrito.objects.get(usuario=usuario.id)
     nuevo_precio_Carrito = 0
     for item in carrito.items.all():
          nuevo_precio_Carrito += item.producto.precio
          carrito.total = nuevo_precio_Carrito
          carrito.save()
     return render(request, 'store/checkout.html',{

          'categorias' : categorias,
          'usuario' : usuario,
          'items_carrito' : productos


     })

     


def registrar_usuario(request):

     form= CreateUserForm()
     if request.method == 'POST':
          form =CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               user= form.cleaned_data.get('username')
               messages.success(request, 'Se a Creado con exito' + user  )
               return redirect(logins)

     context ={'form':form}
     return render(request, 'store/registrar_usuario.html', context)



def logins(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          user =authenticate(request, username=username, password=password)
          if user is not None:
               login (request, user)
               return redirect('store')
          else:
                    messages.info(request, 'el usuario es incorrecto ')
     context ={}
     return render(request,'store/logins.html', context)  


def cerrar_secion(request):
     logout(request)
     return redirect('store')

     
#PRODUCTOS
     

def nuevo_producto(request):
     data = {
          'form':Producto_Form()
     }
     if request.method == 'POST':
          form = Producto_Form(request.POST, request.FILES)
          if form.is_valid():
               form.save()
               messages.success(request, 'Producto Agregado ')
               
          else:
               data["from"] = form     
               
     return render(request, 'store/nuevo_producto.html',data)

def lista_produtos(request):
     producto = Producto.objects.all()
     categorias = Categoria.objects.all()
      
          
     data = {'producto' : producto,'categorias' :categorias}
     return render(request,'store/lista_produtos.html', data)


def editar_produtos(request, id ):
     productos = get_object_or_404(Producto, id=id)
     categorias = Categoria.objects.all()

     data = {
          'form':Producto_Form(instance=productos), 'categorias': categorias
     }
     if request.method == 'POST':
          form = Producto_Form(data=request.POST, instance=productos, files=request.FILES)
          if form.is_valid():
               form.save()
               messages.success(request, 'Producto Modificado ')
               return redirect  ("lista" )
               
          data ['form'] = 'form'

     return render(request, 'store/modificar.html',data) 



def elimanar_producto(request, id):
     productos = get_object_or_404(Producto, id=id)
     productos.delete()
     messages.success(request, 'Producto Eliminado ')
     return redirect  ("lista" )



def ver_detalle(request, id):
    

     object = Producto.objects.get(id = id)

     return render(request, 'store/detalle.html', locals() )



#CATEGORIA
def nueva_categoria(request):
     categorias = Categoria.objects.all()
     data = {
          'form':Categoria_Form(), 'categorias' : categorias 
     }
     if request.method == 'POST':
          form = Categoria_Form(request.POST, request.FILES)
          if form.is_valid():
               form.save()
               messages.success(request, 'Categoria Agregado ')
               
          else:
               data["from"] = form     
               
     return render(request, 'store/nueva_categoria.html', data )


def lista_categoria(request):
     categoria = Categoria.objects.all().order_by('-id')
     categorias = Categoria.objects.all()
     data = {'categoria' : categoria , 'categorias' : categorias}
     return render(request,'store/lista_categoria.html',data)
     

def editar_categoria(request, id ):
     categoria = get_object_or_404(Categoria, id=id)
     categorias = Categoria.objects.all()

     data = {
          'form':Categoria_Form(instance=categoria), 'categorias' : categorias
     }
     if request.method == 'POST':
          form = Categoria_Form(data=request.POST, instance=categoria, files=request.FILES)
          if form.is_valid():
               form.save()
               messages.success(request, 'Categoria Modificado ')
               return redirect  ("listar" )
               
          data ['form'] = 'form'

     return render(request, 'store/modificarcate.html',data ) 




def elimina_categoria(request, id):
     categoria = get_object_or_404(Categoria, id=id)
     categoria.delete()
     messages.success(request, 'Categoria Eliminado ')
     return redirect  ("listar")



def buscador_productos(request):
     busqueda = request.GET['texto']
     productosTitulo = Producto.objects.filter(nombre__icontains = busqueda).all()
     produtosNombre  =  Producto.objects.filter(nombre__icontains = busqueda).all()
     producto  = productosTitulo | produtosNombre
     return render(request, 'store/Buscador.html',{
          'categorias' : Categoria.objects.all(),
          'producto'  : producto,
          'texto_buscado' : busqueda,
          'seccion'   :  'producto que contienen',
          'sin_productos'  : 'No hay producto en la categoria' + busqueda

     })



def categori_productos(request, id):
     categoria = get_object_or_404(Categoria, id=id)
     productos = categoria.productos.filter()
     return render(request, 'store/Buscador.html',
     {
          'categorias' : Categoria.objects.all(),
          'producto': productos,
          'categoria' : categoria.nombre,
          'titulo_seccion' : 'producto de la categoria',
          'sin_productos' : 'No hay productos de la categoria' + categoria.nombre       
     })
