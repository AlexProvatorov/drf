from carts.models import Cart
from goods.models import Book, Tag, Author
from users.models import User

from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = '__all__'


class CartAddSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        exclude = ['id', 'created_at', 'status']


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['count']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['date_joined', 'last_login']


class HistoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
