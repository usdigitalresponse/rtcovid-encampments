from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.reporting import views

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r"visits", views.ReportViewSet)
router.register(r"organizations", views.OrganizationViewSet)
router.register(r"encampments", views.EncampmentViewSet)
urlpatterns = [
    path("api/", include(router.urls)),
    # Encampments
    path("", views.EncampmentListView.as_view(), name="encampment-list"),
    path("encampments/create", views.EncampmentCreateView.as_view()),
    path(
        "encampments/<str:pk>/",
        views.EncampmentDetailView.as_view(),
        name="encampment-detail",
    ),
    # Reporting
    path("reports/create", views.ReportCreateView.as_view(), name="report-create"),
    # Organizations
    path("organizations/create", views.OrganizationCreateView.as_view()),
]
