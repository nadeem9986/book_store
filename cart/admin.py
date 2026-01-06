from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['book', 'quantity', 'session_key', 'added_at']
    list_filter = ['added_at']
    search_fields = ['book__title', 'session_key']
