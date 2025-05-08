from .models import Categories
from django.forms import ModelForm, TextInput

class CategoriesForm(ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description']

    widgets = {
        'name': TextInput(attrs={
            'id': 'category'
        }),
        'description': TextInput(attrs={
            'id': 'description'
        }),
    }