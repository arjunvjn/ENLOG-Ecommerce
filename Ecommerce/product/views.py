from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination

from core.permissions import IsAdmin
from category.models import Category
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_product(request):
    try:
        category_id = request.data['category']
        category = Category.objects.get(id=category_id)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category)
            cache.delete('product_cache')
            return Response({"status":"Success", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":"Error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        data = cache.get('product_cache')
        if not data:
            products = Product.objects.select_related('category').all()
            data = list(products)
            cache.set('product_cache', data, timeout=60*60)
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        filtered_data = data
        if category:
            filtered_data = [data for data in filtered_data if data.category.name.lower() == category.lower()]
        if min_price:
            filtered_data = [data for data in filtered_data if data.price >= float(min_price)]
        if max_price:
            filtered_data = [data for data in filtered_data if data.price <= float(max_price)]
        result_page = paginator.paginate_queryset(filtered_data, request)
        serializer = ProductSerializer(result_page, fields=['id', 'name', 'category', 'price'], many=True)
        result_data = paginator.get_paginated_response(serializer.data).data
        return Response({"status":"Success", "data":result_data})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, id):
    try:
        product = Product.objects.select_related('category').get(id=id)
        serializer = ProductSerializer(product)
        return Response({"status":"Success", "data":serializer.data})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_product(request, id):
    try:
        product = Product.objects.select_related('category').get(id=id)
        category_id = request.data.get('category')
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            if category_id:
                category = Category.objects.get(id=category_id)
                serializer.save(category=category)
            else:
                serializer.save()
            cache.delete('product_cache')
            return Response({"status":"Success", "data":serializer.data})
        return Response({"status":"Error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_product(request, id):
    try:
        Product.objects.get(id=id).delete()
        cache.delete('product_cache')
        return Response({"status":"Success", "message":"Product Deleted"})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)