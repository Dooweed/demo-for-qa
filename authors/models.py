from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name / Полное имя", help_text="Enter the full name of the author / Введите полное имя автора")
    username = models.CharField(max_length=150, unique=True, verbose_name="Username / Имя пользователя", help_text="Unique username for login / Уникальное имя пользователя для входа")
    password = models.CharField(max_length=128, verbose_name="Password / Пароль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At / Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At / Обновлено")
    active = models.BooleanField(default=True, verbose_name="Active / Активен", help_text="Designates whether this author should be treated as active / Указывает, следует ли считать этого автора активным")
    description = models.TextField(null=True, blank=True, verbose_name="Description / Описание", help_text="Short biography or description / Краткая биография или описание")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']
