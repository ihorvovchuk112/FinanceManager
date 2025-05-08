from django.db import models
from django.contrib.auth.models import User
from FinApp.models import Categories

# Create your models here.
class Expense(models.Model):
    name = models.CharField('Назва', max_length=30)
    amount = models.DecimalField('Сума',max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Категорія")
    datetime = models.DateTimeField('Дата/Час',auto_now_add=True)
    description = models.CharField('Опис', max_length=50, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'