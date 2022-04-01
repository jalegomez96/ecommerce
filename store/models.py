from django.db import models
from django.contrib.auth.models import User






class Rol(models.Model):

	nombre_rol = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.nombre_rol
 
class Ciudad(models.Model):
	codigo = models.IntegerField(unique=True) 
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return str(self.id) + ' ' + self.nombre + ' ' + str(self.codigo)

class Persona(models.Model):
	cedula          = models.IntegerField(unique=True)
	nombre          = models.CharField(max_length=50)
	apellidos       = models.CharField(max_length=50)
	telefono        = models.CharField(max_length=15, null= True, blank = True)
	direccion       = models.CharField(max_length=100, null= True, blank = True)
	rol             = models.ForeignKey(Rol, on_delete=models.CASCADE)
	ciudad          = models.ForeignKey(Ciudad, on_delete=models.CASCADE) 
	user 			= models.OneToOneField(User, on_delete=models.CASCADE) 
	# Uno a Uno entre User y Persona, un User Solo tendra una persona asociada

	def __str__(self):
		return self.nombre + ' ' + self.apellidos 

class Categoria (models.Model):
	codigo 				= models.IntegerField(unique=True)
	nombre 				= models.CharField(max_length=50)
	especificaciones 	= models.TextField(max_length=500, null= True, blank = True)  

	def __str__(self):
		return self.nombre 

class Producto (models.Model):
	codigo 				= models.IntegerField(unique=True)
	nombre 				= models.CharField(max_length=30, unique=True)
	precio 				= models.DecimalField(max_digits = 8, decimal_places = 2)
	fecha_vencimiento 	= models.DateField( null= True, blank = True)
	especificaciones 	= models.TextField(max_length = 5000, null= True, blank = True)
	foto                =  models.ImageField(upload_to = 'Producto',blank=True,null=True,verbose_name='Photo')
	foto2               = models.ImageField(upload_to = 'foton',null= True, blank = True)
	foto1               = models.ImageField(upload_to = 'media', null= True, blank = True)
	peso 				= models.CharField(max_length = 5, null= True, blank = True) # 10kg
	categoria 			= models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")

	
		

	def __str__(self):
		return self.nombre

	def  get_precio(self):
		return "{:.2f}".format(self.precio / 100)
	
def upload_gallery_image(instance, filename):
    return f"productos/gallery/{filename}"

class Imagen(models.Model):
	imagen = models.ImageField(upload_to = upload_gallery_image)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="images")

	def __str__ (self):
		return str(self.producto.id) + " " + str(self.producto.nombre) 




ESTADOS=(
	('activo', 'Activo'),
	('cancelado', 'Cancelado'),
	('pagado', 'Pagado'),
)

class Carrito(models.Model):

	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
	total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
	estado = models.CharField(max_length=50, choices=ESTADOS, default='activo')

	def __str__(self) -> str:
		return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"

	def get_raw_subtotal(self):
		total = 0
		for items_carrito in self.items.all():
			total += items_carrito.get_raw_total_item_precio()
		return total



	def get_subtotal(self):
		subtotal = self.get_raw_subtotal()
		return "{:.2f}".format(subtotal / 100)


class Carrito_item(models.Model):
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
	carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
	cantidad = models.IntegerField(default=1)
	subtotal = models.IntegerField(null=True, blank=True, default=0)

	def __str__(self) -> str:
		return f"Id: {self.pk} | Producto: {self.producto.nombre} | Carrito_id: {self.carrito.id} " +"" + str (self.cantidad)

	
	def get_raw_total_item_precio(self):
		return self.cantidad * self.producto.precio
 
	def get_total_item_precio(self):
		precio = self.get_raw_total_item_precio()
		return "{:.2f}".format(precio / 100)



class Factura (models.Model):
	nombre_entidad 		= models.CharField(max_length=30, unique=True, default='Ecommerce Santander')
	fecha_compra 		= models.DateTimeField(auto_now_add = True)
	total 				= models.FloatField(default = 0) 
	iva 				= models.IntegerField()  
	direccion       	= models.CharField(max_length=100)
	cliente				= models.ForeignKey(Persona, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.cliente.cedula) + self.cliente.nombre + ' ' + str(self.id)


class Detalle (models.Model):
	cantidad = models.IntegerField()
	subtotal = models.IntegerField()
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	fatura   = models.ForeignKey(Factura, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.factura.id)+ ' ' + str(self.producto.nombre) + str(self.cantidad) + ' ' + str(self.id)














