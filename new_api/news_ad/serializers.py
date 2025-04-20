from rest_framework import serializers

class NewsRequestSerializer(serializers.Serializer):
    pincode = serializers.CharField(max_length=6)
    product = serializers.CharField(max_length=100) 

