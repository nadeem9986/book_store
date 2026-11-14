from django.test import TestCase

# Create your tests here.


class OrderConfirmationPrivacyTests(TestCase):
    """Regression tests: order confirmations are private to the placing session."""

    def _place_order(self, client, book):
        session = client.session
        session.save()
        from cart.models import CartItem
        CartItem.objects.create(book=book, quantity=1, session_key=session.session_key)
        return client.post('/orders/place-order/', {
            'customer_name': 'Test Person',
            'customer_email': 't@example.com',
            'customer_phone': '9999999999',
            'address': '123 Secret Lane',
        })

    def setUp(self):
        from books.models import Book, Category
        cat = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(title='T', author='A', price=10, category=cat, stock=10)

    def test_placing_session_sees_confirmation(self):
        client = __import__('django.test', fromlist=['Client']).Client()
        response = self._place_order(client, self.book)
        self.assertEqual(response.status_code, 302)
        confirmation_url = response['Location']
        detail = client.get(confirmation_url)
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, 'Test Person')

    def test_other_session_cannot_view_confirmation(self):
        from django.test import Client
        owner = Client()
        response = self._place_order(owner, self.book)
        confirmation_url = response['Location']
        stranger = Client()
        detail = stranger.get(confirmation_url)
        self.assertEqual(detail.status_code, 404)


class AtomicOrderPlacementTests(TestCase):
    """Regression tests: a failed order placement writes no partial order."""

    def setUp(self):
        from books.models import Book, Category
        cat = Category.objects.create(name='Fiction')
        self.book1 = Book.objects.create(title='T1', author='A', price=10, category=cat, stock=10)
        self.book2 = Book.objects.create(title='T2', author='A', price=20, category=cat, stock=10)

    def _seed_cart(self, client, *books):
        session = client.session
        session.save()
        from cart.models import CartItem
        for book in books:
            CartItem.objects.create(book=book, quantity=1, session_key=session.session_key)

    def test_failed_placement_rolls_back_and_keeps_cart(self):
        from unittest.mock import patch
        from django.db import DatabaseError
        from django.test import Client
        from orders.models import Order, OrderItem
        from cart.models import CartItem

        client = Client()
        self._seed_cart(client, self.book1, self.book2)

        with patch('orders.views.OrderItem') as mock_order_item:
            mock_order_item.objects.create.side_effect = DatabaseError('simulated failure')
            response = client.post('/orders/place-order/', {
                'customer_name': 'Test Person',
                'customer_email': 't@example.com',
                'customer_phone': '9999999999',
                'address': '123 Secret Lane',
            })

        # Order save must be rolled back; cart must survive untouched.
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertEqual(CartItem.objects.count(), 2)
        self.assertRedirects(response, '/cart/cart/')

    def test_successful_placement_writes_items_and_clears_cart(self):
        from django.test import Client
        from orders.models import Order, OrderItem
        from cart.models import CartItem

        client = Client()
        self._seed_cart(client, self.book1, self.book2)
        response = client.post('/orders/place-order/', {
            'customer_name': 'Test Person',
            'customer_email': 't@example.com',
            'customer_phone': '9999999999',
            'address': '123 Secret Lane',
        })

        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(CartItem.objects.count(), 0)


class StockDecrementTests(TestCase):
    """Regression tests: placing an order decrements stock and rejects overselling."""

    def setUp(self):
        from books.models import Book, Category
        cat = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(title='T', author='A', price=10, category=cat, stock=5)

    def _seed_cart(self, client, book, quantity):
        session = client.session
        session.save()
        from cart.models import CartItem
        CartItem.objects.create(book=book, quantity=quantity, session_key=session.session_key)

    def _place(self, client):
        return client.post('/orders/place-order/', {
            'customer_name': 'Test Person',
            'customer_email': 't@example.com',
            'customer_phone': '9999999999',
            'address': '123 Secret Lane',
        })

    def test_order_decrements_stock(self):
        from django.test import Client
        client = Client()
        self._seed_cart(client, self.book, 2)
        response = self._place(client)
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 3)

    def test_insufficient_stock_rejects_order_and_keeps_everything(self):
        from django.test import Client
        from orders.models import Order, OrderItem
        from cart.models import CartItem
        client = Client()
        self._seed_cart(client, self.book, 6)  # only 5 in stock
        response = self._place(client)
        self.assertRedirects(response, '/cart/cart/')
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertEqual(CartItem.objects.count(), 1)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 5)

    def test_stock_decrements_per_line(self):
        from django.test import Client
        from books.models import Book, Category
        cat = Category.objects.get(name='Fiction')
        book2 = Book.objects.create(title='T2', author='A', price=20, category=cat, stock=4)
        client = Client()
        self._seed_cart(client, self.book, 2)
        session = client.session
        from cart.models import CartItem
        CartItem.objects.create(book=book2, quantity=1, session_key=session.session_key)
        response = self._place(client)
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        book2.refresh_from_db()
        self.assertEqual(self.book.stock, 3)
        self.assertEqual(book2.stock, 3)
