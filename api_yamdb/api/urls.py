from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    send_confirmation_code,
                    send_token, signup
                    )

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_urls = [
    path('auth/token/', send_token, name='send_token'),
    path('auth/signup/', signup, name='send_confirmation_code'),
    path('auth/code/', send_confirmation_code, name='send_confirmation_code')
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(auth_urls))
]
