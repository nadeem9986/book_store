from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem
from books.models import Book


def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def view_cart(request):
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    session_key = get_session_key(request)
    
    # Check if book already in cart
    cart_item, created = CartItem.objects.get_or_create(
        book=book,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{book.title} added to cart!')
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    session_key = get_session_key(request)
    cart_item = get_object_or_404(CartItem, pk=item_id, session_key=session_key)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('view_cart')


def update_quantity(request, item_id):
    if request.method == 'POST':
        session_key = get_session_key(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, session_key=session_key)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('view_cart')
