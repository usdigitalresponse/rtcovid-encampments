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
    # API
    path("api/", include(router.urls)),
    # Encampments
    path("", views.EncampmentListView.as_view(), name="encampment-list"),
    path(
        "encampments/<str:pk>/",
        views.EncampmentDetailView.as_view(),
        name="encampment-detail",
    ),
    # Regions
    path(
        "regions/<str:slug>/", views.EncampmentListView.as_view(), name="region-detail"
    ),
    # Filters
    path(
        "filters/<str:mode>/",
        views.EncampmentListView.as_view(),
        name="encampment-list-filtered",
    ),
    # Reporting
    path("reports/create", views.ReportCreateView.as_view(), name="report-create"),
    path("tasks/", views.CreateTask.as_view(), name="task-create"),
    path("tasks/<str:pk>/complete", views.CompleteTask.as_view(), name="task-complete"),
]
