from django.contrib import admin
from django.contrib.admin import ModelAdmin

from BooksApp.models import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ["title", "author", "publication_date", "user"]


