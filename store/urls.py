from django.contrib.auth import login
from django.urls import path
from  .import views

urlpatterns = [
	
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('logins/', views.logins, name='logins' ),
	path('cerrar/', views.cerrar_secion, name='cerrar' ),
	path('registrar_usuario/', views.registrar_usuario, name='registrar'),

	
	#producto
	path('producto/',views.nuevo_producto, name='producto'),
	path('lista/',views.lista_produtos, name='lista'),
	path('editar/<id>/',views.editar_produtos, name='editar'),
	path('eliminar/<id>/',views.elimanar_producto, name='eliminar'),
	path('detalle/<id>/',views.ver_detalle, name='detalle'),
	

	#categoria
	path('agregar_categoria/',views.nueva_categoria, name='categoria'),
	path('listar/',views.lista_categoria, name='listar'),
	path('edita/<id>/',views.editar_categoria, name='edita'),
	path('elimina/<id>/',views.elimina_categoria, name='elimina'),
	path('buscar/',views.buscador_productos, name='buscador_productos'),
	path('categoria/<id>/',views.categori_productos, name='categori_productos'),


	path('agregar_item/<id>/',views.agregar_item, name='agregar_item'),
	path('eliminar_carrito/<id>/',views.eliminar_carrito, name='eliminar_carrito'),
	path('increase-cantidad/<id>/',views.IncreaseCantidad, name='increase-cantidad'),
	path('decrease-cantida/<id>/',views.DecreaseCantidad, name='decrease-cantida'),


	
	
	



]