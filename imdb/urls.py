from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MovieViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
]
