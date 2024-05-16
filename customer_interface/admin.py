from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Orders, OrderItem, Sales, CustomUser

admin.site.register(Orders)
admin.site.register(OrderItem)
admin.site.register(Sales)
admin.site.register(CustomUser)