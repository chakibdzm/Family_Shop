from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer
from rest_framework import serializers


class CustomerCreateSerializer(BaseUserCreateSerializer):
    birth_date = serializers.DateField(read_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'birth_date']


class CustomerSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields=['id','username','email','first_name','last_name']