from rest_framework import serializers
from .models import Product, Category, ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['size', 'price']

class ProductSerializers(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)  # Related name 'variants' is used

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'product_image', 'variants']

class UpdateProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'product_image')

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.product_image = validated_data.get('product_image', instance.owner_id)
        instance.save()
        return instance

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UpdateCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance
