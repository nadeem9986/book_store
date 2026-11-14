from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import DatabaseError, transaction
from django.db.models import F
from books.models import Book
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import CartItem
from cart.views import get_session_key


class InsufficientStockError(Exception):
    """Raised when a cart line asks for more than the book has in stock."""

    def __init__(self, book):
        self.book = book
        super().__init__(f'Not enough stock for "{book.title}".')


def place_order(request):
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    total = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.total_amount = total
                    order.session_key = session_key
                    order.save()

                    # Create order items, decrementing stock atomically
                    for cart_item in cart_items:
                        updated = Book.objects.filter(
                            pk=cart_item.book.pk,
                            stock__gte=cart_item.quantity,
                        ).update(stock=F('stock') - cart_item.quantity)
                        if not updated:
                            raise InsufficientStockError(cart_item.book)
                        OrderItem.objects.create(
                            order=order,
                            book=cart_item.book,
                            quantity=cart_item.quantity,
                            price=cart_item.book.price
                        )

                    # Clear cart
                    cart_items.delete()
            except InsufficientStockError as exc:
                messages.error(
                    request,
                    f'Sorry, "{exc.book.title}" does not have enough stock '
                    'for that quantity. Please update your cart.'
                )
                return redirect('view_cart')
            except DatabaseError:
                messages.error(
                    request,
                    'Something went wrong while placing your order. '
                    'Your cart is unchanged - please try again.'
                )
                return redirect('view_cart')

            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'place_order.html', {'form': form, 'cart_items': cart_items, 'total': total})


def order_confirmation(request, order_id):
    session_key = get_session_key(request)
    order = get_object_or_404(Order, pk=order_id, session_key=session_key)
    return render(request, 'order_confirmation.html', {'order': order})
