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
        self.book = Book.objects.create(title='T', author='A', price=10, category=cat)

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
