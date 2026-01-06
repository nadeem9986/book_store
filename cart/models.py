from django.db import models
from books.models import Book


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_key = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.book.title} x {self.quantity}"
    
    def get_total_price(self):
        return self.book.price * self.quantity
    
    class Meta:
        ordering = ['-added_at']
