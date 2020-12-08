from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import ApiUser, Content, Category


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email', )


class ApiUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ApiUser
        fields = ('is_premium', 'user',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class ContentSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Content
        fields = '__all__'
