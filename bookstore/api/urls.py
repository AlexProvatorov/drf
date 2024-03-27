from django.urls import path, include

from rest_framework import routers

from .views import UsersHistories, CartUpdate, CartAdd, CartDelete
from .views import BookViewSet, TagViewSet, AuthorViewSet, CartView, \
    UserViewSet, UserHistory

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'tags', TagViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('user-history/', UserHistory.as_view()),
    path('users-histories/', UsersHistories.as_view()),
    path('cart/', CartView.as_view()),
    path('cart-update/<int:pk>/', CartUpdate.as_view()),
    path('cart-add/', CartAdd.as_view()),
    path('cart-delete/<int:pk>/', CartDelete.as_view()),
]
