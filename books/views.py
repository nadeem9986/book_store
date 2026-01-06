from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category


def home(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})


def books_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    books = Book.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories, 'selected_category': category})
