from django.urls import path

from . import views

urlpatterns = [
    path('get_cart_items', views.get_cart_items, name='get_cart_items'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('increment_quantity/<int:id>', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:id>', views.decrement_quantity, name='decrement_quantity'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('place_order', views.place_order, name='place_order'),
    path('update_status/<id>',views.update_status, name='update_status'),
    path('', views.view_orders, name='view_orders')    
]