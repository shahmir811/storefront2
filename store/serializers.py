from decimal import Decimal
from rest_framework import serializers


from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'inventory',
                  'unit_price', 'description', 'price_with_tax', 'collection']
        extra_kwargs = {
            "title": {
                "error_messages": {
                    "required": "Product title is required"
                }
            },
            "unit_price": {
                "error_messages": {
                    "required": "Mention product unit price"
                }
            }
        }

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    # collection = CollectionSerializer()
    # collection = serializers.StringRelatedField()
    # collection = serializers.PrimaryKeyRelatedField(
    # queryset=Collection.objects.all()
    # )

    def calculate_tax(self, product: Product):
        # return product.unit_price * Decimal(1.1)
        return Decimal(format(product.unit_price * Decimal(1.1), '0.2f'))

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords donot match')
    #     return data
