from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from api.permissions import IsAdminOrReadOnly, IsOwnerUser
from carts.models import Cart
from goods.models import Book, Tag, Author
from users.models import User

from api.serializers import (BookSerializer, TagSerializer, AuthorSerializer,
                             CartSerializer, UserSerializer,
                             HistoryUserSerializer, CartUpdateSerializer,
                             CartAddSerializer
                             )


class BookAPIListPagination(PageNumberPagination):
    """
    Пагинатор для BookViewSet. Для всего остального DEFAULT_PAGINATION_CLASS в
    settings.py
    """
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookViewSet(ModelViewSet):
    """
    CRUD EndPoint для работы над книгами. Админ может все, юзеры только читать.
    """
    queryset = Book.item_objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = BookAPIListPagination
    throttle_classes = [UserRateThrottle, AnonRateThrottle,]


class TagViewSet(ModelViewSet):
    """
    CRUD EndPoint для работы над тегами. Админ может все, юзеры только читать.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
    throttle_classes = [UserRateThrottle, AnonRateThrottle,]


class AuthorViewSet(ModelViewSet):
    """
    CRUD EndPoint для работы над авторами. Админ может все, юзеры только читать.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly, )
    throttle_classes = [UserRateThrottle, AnonRateThrottle,]


class CartViewSet(ModelViewSet):
    """
    CRUD EndPoint для работы над корзиной.
    """
    queryset = Cart.cart_objects.filter(status="PENDING")
    serializer_class = CartSerializer
    permission_classes = [IsOwnerUser | IsAdminUser]


class UserViewSet(ModelViewSet):
    """
    CRUD EndPoint для работы над пользователями, только для админа.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

#
# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# @throttle_classes([UserRateThrottle])
# def history_user_list(request, format=None):
#     # EndPoint для отображения списка историй пользователей. Только чтение и
#     # только для админа.
#     queryset = Cart.cart_objects.filter(status="COMPLETED").order_by(
#         "created_at"
#     )
#     serializer = HistoryUserSerializer(queryset, many=True)
#     return Response(serializer.data)


class UserHistory(generics.ListAPIView):
    """
    EndPoint для отображения истории текущего пользователя.
    """
    serializer_class = HistoryUserSerializer
    permission_classes = (IsOwnerUser, )
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Cart.cart_objects.filter(
            customer=user, status="COMPLETED"
        ).prefetch_related("customer", "item")


class UsersHistories(generics.ListAPIView):
    """
    EndPoint для отображения историй покупок всех пользователей. Только чтение
    и только для админа.
    """
    queryset = Cart.cart_objects.filter(status='COMPLETED')
    serializer_class = HistoryUserSerializer
    permission_classes = (IsAdminUser, )
    throttle_classes = [UserRateThrottle]


class CartView(generics.ListAPIView):
    """
    EndPoint предоставляющий владельцу возможность просматривать свою корзину.
    """
    serializer_class = CartSerializer
    permission_classes = (IsOwnerUser, )
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Cart.cart_objects.filter(
            Q(status="PENDING") | Q(status="CANCELLED") | Q(status=""),
            customer=user
        ).prefetch_related("customer", "item")


class CartUpdate(generics.UpdateAPIView):
    """
    EndPoint позволяющий юзеру изменять счетчик товара в корзине или удалять их.
    """
    queryset = Cart.cart_objects.filter(Q(status="CANCELLED") | Q(status=""))
    serializer_class = CartUpdateSerializer
    permission_classes = (IsOwnerUser, )
    throttle_classes = [UserRateThrottle]


class CartAdd(generics.CreateAPIView):
    """
    EndPoint позволяющий юзеру добавлять товар в корзину.
    """
    serializer_class = CartAddSerializer
    permission_classes = (IsOwnerUser, )
    throttle_classes = [UserRateThrottle]


class CartDelete(generics.DestroyAPIView):
    """
    EndPoint позволяющий юзеру удалять товары из корзины.
    """
    queryset = Cart.cart_objects.filter(Q(status="CANCELLED") | Q(status=""))
    serializer_class = CartSerializer
    permission_classes = (IsOwnerUser, )
    throttle_classes = [UserRateThrottle]
