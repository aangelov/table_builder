from django.urls import path, include
from rest_framework import routers
from .views import TableViewSet

router = routers.DefaultRouter()
router.register(r'table', TableViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]