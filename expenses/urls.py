from django.urls import path
from . import views
urlpatterns = [
    path('expenses', views.expenses, name='expenses'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('expenses/<int:pk>/update_expense', views.ExpenseUpdateView.as_view(), name='update_expense'),
    path('expenses/<int:pk>/delete_expense', views.ExpenseDeleteView.as_view(), name='delete_expense')
]