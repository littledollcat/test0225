from django.db import models
from django.contrib import admin

# Create your models here.

class Products(models.Model):
    stock_pcs = models.IntegerField()
    price = models.IntegerField()
    shop_id = models.CharField(max_length=20)
    vip = models.BooleanField()

class Orders(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='product_id')
    qty = models.IntegerField()
    price = models.IntegerField()
    shop_id = models.CharField(max_length=20)
    CustomerID = models.IntegerField()

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Products._meta.fields]

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Orders._meta.fields]
