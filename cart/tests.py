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


class CartActionsRequirePostTests(TestCase):
    """Regression tests: add/remove change state, so GET must not perform them."""

    def setUp(self):
        from books.models import Book, Category
        from cart.models import CartItem
        cat = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(title='T', author='A', price=10, category=cat)
        session = self.client.session
        session.save()
        self.session_key = session.session_key
        self.item = CartItem.objects.create(book=self.book, quantity=1, session_key=self.session_key)

    def test_get_add_to_cart_does_not_create_item(self):
        from cart.models import CartItem
        response = self.client.get(f'/cart/add/{self.book.id}/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(CartItem.objects.filter(session_key=self.session_key).count(), 1)

    def test_post_add_to_cart_adds_item(self):
        from cart.models import CartItem
        response = self.client.post(f'/cart/add/{self.book.id}/')
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 2)  # existing line merges, +1

    def test_get_remove_keeps_item(self):
        from cart.models import CartItem
        response = self.client.get(f'/cart/remove/{self.item.id}/')
        self.assertEqual(response.status_code, 405)
        self.assertTrue(CartItem.objects.filter(pk=self.item.pk).exists())

    def test_post_remove_deletes_item(self):
        from cart.models import CartItem
        response = self.client.post(f'/cart/remove/{self.item.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(pk=self.item.pk).exists())
