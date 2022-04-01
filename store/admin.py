from django.contrib import admin
from .models import *
from .models import  Imagen

class CategoriAdmin(admin.ModelAdmin):
    list_display = ('codigo'  , 'nombre', 'especificaciones')
    search_fields =['nombre']
    list_filter = ('nombre',)

class ProductoAdmin(admin.ModelAdmin):
    list_display   =   ('codigo', 'nombre', 'precio', 'fecha_vencimiento' ,'especificaciones', 'peso', 'categoria')
    search_fields  =   ['nombre','codigo']
    list_editable  =   ['precio']

class ImageInline(admin.TabularInline):
    model = Imagen

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]


admin.site.register(Rol)
admin.site.register(Ciudad)
admin.site.register(Persona)
admin.site.register(Categoria,CategoriAdmin)
#admin.site.register(Producto,ProductoAdmin)
admin.site.register(Factura)
admin.site.register(Detalle)
admin.site.register(Imagen)
admin.site.register(Carrito)
admin.site.register(Carrito_item)


#admin.site.register(Customer)
#admin.site.register(Product)
#admin.site.register(Order)
#admin.site.register(OrderItem)
#admin.site.register(ShippingAddress)

