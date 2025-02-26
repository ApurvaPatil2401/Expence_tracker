from django import forms
from .models import Book, BookCategory

class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publishing_date', 'category', 'distribution_expense']

class UploadFileForm(forms.Form):
    file = forms.FileField()

