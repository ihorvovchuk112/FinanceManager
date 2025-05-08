from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('categories', views.categories, name = 'categories'),
    path('categories/add', views.add_category, name='add_category'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),

]