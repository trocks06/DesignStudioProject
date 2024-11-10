from django.db import models
from django.contrib.auth.models import AbstractUser

class AdvUser(AbstractUser):
    patronymic = models.CharField(max_length=50, blank=True)
    is_employer = models.BooleanField(default=False, verbose_name='Статус сотрудника')

    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(max_length=100, blank=False, unique=True, verbose_name='Название категории')
    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

class Application(models.Model):
    app_name = models.CharField(max_length=100, blank=False, verbose_name='Название заявки')
    app_description = models.TextField(blank=False, verbose_name='Описание заявки')
    app_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, verbose_name='Категория заявки')
    app_date_created = models.DateTimeField(auto_now_add=True)
    app_image = models.ImageField(upload_to='app_images/', blank=False, verbose_name='Фото помещения или его план')
    app_publisher = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, blank=False, null=True, related_name='applications_published')

    design_image = models.ImageField(upload_to='design_images/', null=True, blank=True)
    design_publisher = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications_designs')

    APP_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('d', 'Выполнено'),
    )
    status = models.CharField(max_length=1, choices=APP_STATUS, blank=False, default='n')
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.app_name