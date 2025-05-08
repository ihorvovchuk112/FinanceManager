from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Categories
from .forms import ExpenseForm
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.
@login_required
def expenses(request):
    expenses_list = Expense.objects.filter(user=request.user).order_by('-datetime')
    return render(request, 'expenses/expenses.html', {'expenses_list': expenses_list})



def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            new_cat_name = form.cleaned_data.get('new_category')
            if new_cat_name:
                category, created = Categories.objects.get_or_create(
                    name=new_cat_name,
                    user=request.user
                )
            else:
                category = form.cleaned_data['category']
            expense = form.save(commit=False)
            expense.user = request.user
            expense.category = category
            expense.save()
            return redirect('expenses')
    else:
        form = ExpenseForm(user=request.user)

    user_categories = Categories.objects.filter(user=request.user)
    return render(request, 'expenses/add_expense.html', {
        'form': form,
        'user_categories': user_categories,
    })

class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'expenses/add_expense.html'
    form_class = ExpenseForm
    success_url = '/expenses'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user 
        return kwargs
    
class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = '/expenses'
    template_name = 'FinApp/delete_template.html'