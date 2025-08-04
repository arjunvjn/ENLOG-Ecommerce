from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_products, name='get_products'),
    path('create', views.create_product, name='create_product'),
    path('update/<int:id>', views.update_product, name='update_product'),
    path('delete/<int:id>', views.delete_product, name='delete_product'),
    path('<int:id>', views.get_product, name='get_product')    
]