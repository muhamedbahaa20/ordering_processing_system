from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'balance']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer(
            username=validated_data['username'],
            email=validated_data['email'],
            balance=validated_data.get('balance', 0.00)  # Default balance if not provided
        )
        customer.set_password(validated_data['password'])  # Hash the password
        customer.save()
        return customer