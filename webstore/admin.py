from django.contrib import admin

from webstore.models import *

class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name', 'category') 

class EventAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name', 'category') 

admin.site.register(Catalog)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)

admin.site.register(Photo)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory)


