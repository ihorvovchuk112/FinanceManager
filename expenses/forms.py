from .models import Expense, Categories
from django.forms import ModelForm, NumberInput, TextInput, Select, CharField

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','name', 'category', 'description']
    
    
    new_category = CharField(
        max_length=100, 
        required=False,
        label="Нова категорія",
        widget=TextInput(attrs={'class': 'custom-input'})
    )
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.filter(user=user)

    widgets = {
        'amount': NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00'
        }),
        'name': TextInput(attrs={
            'id': 'name'
        }),
        'description': TextInput(attrs={
            'id': 'description'
        }),
        'category': Select(attrs={'class': 'custom-input'}),
    }