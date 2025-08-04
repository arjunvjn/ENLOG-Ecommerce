from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from product.models import Product
from user.models import CustomUser
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer
from core.permissions import IsAdmin
from core.views import notify_user

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_items(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        items = OrderItem.objects.select_related('user', 'product').filter(user=user, order__isnull=True)
        serializer = OrderItemSerializer(items, many=True)
        return Response({"status":"Success", "data":serializer.data})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        user = CustomUser.objects.get(id=request.user.id)
        item = OrderItem.objects.filter(user=user, product=product, order__isnull=True).first()
        update_flag = False
        if item and product.stock > item.quantity:
            item.quantity += 1
            item.save()
            update_flag = True
        elif product.stock > 0:
            OrderItem.objects.create(user=user, product=product)
            update_flag = True
        if update_flag:
            return Response({"status":"Success", "message":"Added to Cart"}, status=status.HTTP_201_CREATED)
        return Response({"status":"Error", "message":"Product Out of Stock"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def increment_quantity(request, id):
    try:
        item = OrderItem.objects.get(id=id)
        product = Product.objects.get(id=item.product.id)
        if product.stock > item.quantity:
            item.quantity += 1
            item.save()
            return Response({"status":"Success"})
        return Response({"status":"Error", "message":"Product Out of Stock"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def decrement_quantity(request, id):
    try:
        item = OrderItem.objects.get(id=id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
        return Response({"status":"Success"})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, id):
    try:
        OrderItem.objects.get(id=id).delete()
        return Response({"status":"Success", "message":"Removed from Cart"})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        items = OrderItem.objects.select_related('product').filter(user=user,order__isnull=True)
        if len(items) > 0:
            order = Order.objects.create(user=user)
            unplaced_items = []
            total_price = 0
            for item in items:
                product = Product.objects.get(id=item.product.id)
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    total_price += (item.quantity * product.price)
                    product.save()
                    item.order = order
                    item.save()
                else:
                    unplaced_items.append(product.name)
            order.total_price = total_price
            order.save()
            cache.delete('product_cache')
            return Response({"status":"Success", "message":"Placed Order", "unplaced_items": unplaced_items})
        return Response({"status":"Error", "message":"No Order to be Placed"})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_orders(request):
    try:
        if request.user.role == 'user':
            user = CustomUser.objects.get(id=request.user.id)
            orders = Order.objects.prefetch_related('products').filter(user=user)
            serializer = OrderSerializer(orders, many=True)
        else:
            orders = Order.objects.prefetch_related('products').all()
            serializer = OrderSerializer(orders, many=True)
        return Response({"status":"Success", "data":serializer.data})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PATCH'])
@permission_classes([IsAdmin])
def update_status(request, id):
    try:
        status_update = {'pending': 'shipped', 'shipped': 'delivered'}
        order = Order.objects.select_related('user').get(id=id)
        if not status_update[order.status]:
            if order.status == 'delivered':
                return Response({"status":"Error", "message":"Order is already Delivered"})
            else:
                return Response({"status":"Error", "message":"Issue in Status"})
        order.status = status_update[order.status]
        order.save()
        notify_user(order.user.id, f'Your Order (order_id: {order.id}) has been {order.status}')
        return Response({"status": "notification sent"})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)