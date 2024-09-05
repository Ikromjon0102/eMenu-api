from rest_framework import serializers
from .models import Cafes

class CafesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cafes
        fields = '__all__'

class UpdateCafesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafes
        fields = ('id', 'name', 'owner_id', 'location', 'description', 'phone_number', 'logo', 'start_time', 'modified')


    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.owner_id = validated_data.get('owner_id', instance.owner_id)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.modified = validated_data.get('modified', instance.modified)
        instance.save()
        return instance
    