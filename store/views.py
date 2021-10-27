# from math import prod
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from store import serializers


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Deserialze incoming ovject
        serializer = ProductSerializer(data=request.data)
        # Validating request below
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validate_data
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({
                'error': 'Product cannot be deleted because it is associated with an order item'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response('Product deleted', status=status.HTTP_204_NO_CONTENT)


#################################################
# Collections method

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        collections = Collection.objects.annotate(
            products_count=Count('products')).all().order_by('id')
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({
                'error': 'Collection cannot be deleted because it is associated with product'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection.delete()
        return Response('Collection deleted', status=status.HTTP_204_NO_CONTENT)
