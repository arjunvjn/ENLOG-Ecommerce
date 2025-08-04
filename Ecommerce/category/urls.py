from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_categories, name='get_categories'),
    path('create', views.create_category, name='create_category'),
    path('update/<int:id>', views.update_category, name='update_category'),
    path('delete/<int:id>', views.delete_category, name='delete_category'),    
]