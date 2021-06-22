from django.contrib import admin
from .models import customer,product,cart,orderplaced
from django.utils.html import format_html
from django.urls import reverse


@admin.register(customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['id','name','locality','city','zipcode','state']


@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discount_price','description','brand','catagory','product_image']


@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']



@admin.register(orderplaced)
class orderplacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','customer_info','product','product_info','quantity','ordered_date','status']

    def customer_info(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)

    def product_info(self,obj):
        link=reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
