from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from .models import Categories
from expenses.models import Expense
from .forms import CategoriesForm
from django.db.models import Sum, Max
from django.utils import timezone

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        now = timezone.now()
        today = Expense.objects.filter(
                        user=request.user, datetime__year=now.year, datetime__month=now.month, datetime__day=now.day)
        current_month_expenses = Expense.objects.filter(
                        user=request.user,
                        datetime__year=now.year,
                        datetime__month=now.month
                    )
        today_expenses = today.aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = current_month_expenses.order_by('-datetime')[:5]
        max_expense = current_month_expenses.aggregate(Max('amount'))['amount__max'] or 0
        by_category = (
                current_month_expenses
                .values('category__name')
                .annotate(total=Sum('amount'))
            )
        context = {
                'recent_expenses': expenses,
                'today_expenses': today_expenses,
                'max_expense': max_expense,
                'expenses_by_category': by_category,
            }

        return render(request, 'FinApp/homepage.html', context)
    else:
        return render(request, 'FinApp/welcome.html')

@login_required
def categories(request):
    categories_list = Categories.objects.filter(user=request.user)
    return render(request, 'FinApp/categories.html', {'categories_list': categories_list})

def add_category(request):
    error = ''

    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories')
        else:
            error = "Помилка"

    form = CategoriesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'FinApp/add_category.html', data)

class CategoryDetailView(DetailView):
    model = Categories
    template_name = 'FinApp/category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        # Обмежити доступ лише до категорій користувача
        return Categories.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = Expense.objects.filter(
            category=self.object,
            user=self.request.user
        )
        return context



class CategoryUpdateView(UpdateView):
    model = Categories
    template_name = 'FinApp/add_category.html'
    form_class = CategoriesForm

class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = '/categories'
    template_name = 'FinApp/delete_template.html'


class AnalyticsView(TemplateView):
    template_name = 'FinApp/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            now = timezone.now()

            current_month_expenses = Expense.objects.filter(
                user=user,
                datetime__year=now.year,
                datetime__month=now.month
            )

            expenses = current_month_expenses.order_by('-datetime')[:5]
            total = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            max_expense = current_month_expenses.aggregate(Max('amount'))['amount__max'] or 0

            by_category = (
                current_month_expenses
                .values('category__name')
                .annotate(total=Sum('amount'))
            )

            context.update({
                'recent_expenses': expenses,
                'total_expenses': total,
                'max_expense': max_expense,
                'expenses_by_category': by_category,
            })
        return context
