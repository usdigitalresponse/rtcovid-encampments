from django.conf.urls import url
from django.urls import include, path

# Create a router and register our viewsets with it.
from rest_framework.routers import DefaultRouter

from apps.reporting import views

router = DefaultRouter()
router.register(r'visits', views.ReportViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'encampments', views.EncampmentViewSet)
urlpatterns = [
    path('api/', include(router.urls)),

    # Encampments
    path('encampments/', views.EncampmentListView.as_view(), name='encampment-list'),
    path('encampments/create', views.EncampmentCreateView.as_view()),

    # Reporting
    path('reports/<str:encampment>/', views.ReportListView.as_view(), name='report-list'),
    path('reports/create', views.ReportCreateView.as_view()),

    # Organizations
    path('organizations/create', views.OrganizationCreateView.as_view())


]