from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from core.permissions import IsAdmin
from .models import Category
from .serializers import CategorySerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('category_cache')
            return Response({"status":"Success", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":"Error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    try:
        data = cache.get('category_cache')
        if not data:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            data = serializer.data
            cache.set('category_cache', data, timeout=60*60)
        return Response({"status":"Success", "data":data})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete('category_cache')
            return Response({"status":"Success", "data":serializer.data})
        return Response({"status":"Error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_category(request, id):
    try:
        Category.objects.get(id=id).delete()
        cache.delete('category_cache')
        return Response({"status":"Success", "message":"Category Deleted"})
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)