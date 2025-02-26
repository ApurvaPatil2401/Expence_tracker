from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from .models import Book, BookCategory
from .forms import BookForm, BookCategoryForm
from .utils import import_books_from_excel

# 🏠 HOME PAGE
def home(request):
    return render(request, 'books/home.html')

# 📌 CATEGORY CRUD OPERATIONS
def category_list(request):
    categories = BookCategory.objects.all()
    return render(request, "books/category_list.html", {"categories": categories})

def add_category(request):
    if request.method == "POST":
        form = BookCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = BookCategoryForm()
    return render(request, "books/category_form.html", {"form": form})

def edit_category(request, category_id):
    category = get_object_or_404(BookCategory, id=category_id)
    if request.method == "POST":
        form = BookCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = BookCategoryForm(instance=category)
    return render(request, "books/category_form.html", {"form": form})

def delete_category(request, category_id):
    category = get_object_or_404(BookCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'books/category_confirm_delete.html', {'category': category})

# 📘 BOOK CRUD OPERATIONS
def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, "books/book_form.html", {"form": form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# 📊 REPORT VIEW
def report_view(request):
    report_data = Book.objects.values('category__name').annotate(total_expense=Sum('distribution_expense'))
    report_dict = {item['category__name']: item['total_expense'] for item in report_data}
    return render(request, "books/report.html", {"report_data": report_dict})

# 📂 FILE UPLOAD FUNCTIONALITY (IMPORT BOOKS FROM EXCEL)
def upload_books(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        import_books_from_excel(file)
        return HttpResponse("Books imported successfully!")
    return render(request, 'books/upload_books.html')

import pandas as pd
from .forms import UploadFileForm

def import_books(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                category, created = BookCategory.objects.get_or_create(name=row["Category"])
                Book.objects.create(
                    title=row["Title"],
                    author=row["Author"],
                    publishing_date=row["Publishing Date"],
                    category=category,
                    distribution_expense=row["Distribution Expense"]
                )

            return redirect('book_list')

    else:
        form = UploadFileForm()

    return render(request, "books/upload.html", {"form": form})
