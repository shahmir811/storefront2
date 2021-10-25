from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


@api_view(('GET', 'POST'))
def product_list(request):

    if request.method == 'GET':
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # Deserialze incoming ovject
        serializer = ProductSerializer(data=request.data)
        # Validating request below
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validate_data
        return Response('ok')


@api_view(('GET',))
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

    # TODO: Give better 404 response


#################################################
# Collections method

@api_view(('GET',))
def collection_detail(request, pk):
    return Response('ok')
