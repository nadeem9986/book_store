from django.test import TestCase

# Create your tests here.


class UpdateQuantityValidationTests(TestCase):
    """Regression tests: non-numeric quantities are rejected, not a 500."""

    def setUp(self):
        from books.models import Book, Category
        from cart.models import CartItem
        cat = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(title='T', author='A', price=10, category=cat)
        session = self.client.session
        session.save()
        self.item = CartItem.objects.create(book=self.book, quantity=2, session_key=session.session_key)

    def test_non_numeric_quantity_does_not_crash(self):
        response = self.client.post(f'/cart/update/{self.item.id}/', {'quantity': 'abc'})
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 2)

    def test_zero_quantity_removes_item(self):
        from cart.models import CartItem
        self.client.post(f'/cart/update/{self.item.id}/', {'quantity': '0'})
        self.assertFalse(CartItem.objects.filter(pk=self.item.pk).exists())
