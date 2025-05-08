from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Categories(models.Model):
    name = models.CharField('Назва', max_length=20)
    description = models.CharField('Опис', max_length=60, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/categories/{self.id}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'