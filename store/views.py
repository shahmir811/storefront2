# from math import prod
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):

    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({
                'error': 'Product cannot be deleted because it is associated with an order item'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response('Product deleted', status=status.HTTP_204_NO_CONTENT)


#################################################
# Collections method

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all().order_by('id')

    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all().order_by('id')
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Product, pk=pk)
        if collection.products.count() > 0:
            return Response({
                'error': 'Collection cannot be deleted because it is associated with product'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection.delete()
        return Response('Collection deleted', status=status.HTTP_204_NO_CONTENT)
