from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'active', 'created_at')
    search_fields = ('username', 'full_name')
    list_filter = ('active',)
