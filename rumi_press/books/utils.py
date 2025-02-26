import pandas as pd
from .models import Book, BookCategory

def import_books_from_excel(file):
    #file_path='C:/Users/dell/Downloads/book_data.xlsx'
    df = pd.read_excel(file)
    print("Excel data:")
    print(df.head())
    if df.empty:
        print("No data found in the excel file")
        return
    for _, row in df.iterrows():
        try:
            category, _ = BookCategory.objects.get_or_create(name=row['Category'])
            Book.objects.create(
                title=row['Title'],
                author=row['Author'],
                publishing_date=row.get("Publishing Date",None),
                category=category,
                distribution_expense = row.get("Distribution Expense")  # Use .get() to avoid KeyError

            )

            book.save()
            print("Added:{book.}")
        except Exception as e:
            print(f"Error occurred while importing data: {e}")
