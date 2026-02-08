from django.db import models
from authors.models import Author

class PostStatus(models.IntegerChoices):
    DRAFT = 0, 'Draft / Черновик'
    PUBLISHED = 1, 'Published / Опубликовано'
    ARCHIVED = 2, 'Archived / Архивно'

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title / Заголовок", help_text="Title of the post / Заголовок поста")
    content = models.TextField(verbose_name="Content / Содержание", help_text="Main content of the post / Основное содержание поста")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts', verbose_name="Author / Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At / Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At / Обновлено")
    status = models.IntegerField(choices=PostStatus.choices, default=PostStatus.DRAFT, verbose_name="Status / Статус")

    def __str__(self):
        return self.title
