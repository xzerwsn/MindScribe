from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'featured')
    list_editable = ('featured',)  # Позволяет редактировать прямо в списке
    list_filter = ('featured',)  # Добавляет фильтр