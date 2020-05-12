from django.conf.urls import url
from django.urls import include, path

# Create a router and register our viewsets with it.
from rest_framework.routers import DefaultRouter

from apps.reporting import views

router = DefaultRouter()
router.register(r'visits', views.VisitViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'encampments', views.EncampmentViewSet)
urlpatterns = [
    path('', include(router.urls)),
]