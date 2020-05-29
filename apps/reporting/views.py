from datetime import date

import django_tables2 as tables
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseCreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.reporting.forms import date_picker
from apps.reporting.forms import ScheduleVisitForm
from apps.reporting.forms import TaskForm
from apps.reporting.models import Encampment
from apps.reporting.models import Organization
from apps.reporting.models import Region
from apps.reporting.models import Report
from apps.reporting.models import ScheduledVisit
from apps.reporting.models import Task
from apps.reporting.serializers import EncampmentSerializer
from apps.reporting.serializers import OrganizationSerializer
from apps.reporting.serializers import ReportSerializer


class ReportingBaseView:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not "url_context" in context:
            context["url_context"] = ""
        return context


class EncampmentListView(ReportingBaseView, ListView):
    model = Encampment

    def get_queryset(self):
        if self.kwargs.get("slug", None):
            self.nav_context = self.kwargs["slug"]
            queryset = self.model._default_manager.filter(
                region__slug=self.kwargs["slug"]
            )
        elif self.kwargs.get("mode", None):
            self.nav_context = self.kwargs["mode"]
            if self.kwargs["mode"] == "tasked":
                queryset = self.model._default_manager.tasked()
            elif self.kwargs["mode"] == "delayed":
                queryset = self.model._default_manager.delayed()
        else:
            self.nav_context = ""
            queryset = self.model._default_manager.all()

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            "not_visited_14": Encampment.not_visited_in(14).count(),
            "visits_7": Report.last_n(7).count(),
            "visits_31": Report.last_n(31).count(),
            "visits_14": Report.last_n(14).count(),
            "pending_tasks": Task.objects.filter(completed=None).count(),
            "table": EncampmentTable(self.object_list),
            "regions": Region.objects.all(),
            "nav_context": self.nav_context,
        }
        return {**context, **extra_context}


class HybridDate(tables.Column):
    pass


class EncampmentTable(tables.Table):
    name = tables.Column(linkify=True)
    location = tables.Column()

    last_visit = HybridDate(accessor="last_report.date")
    next_visit = HybridDate(accessor="next_visit.date")

    tasks = tables.Column(accessor="open_tasks.count")


class EncampmentDetailView(ReportingBaseView, DetailView):
    model = Encampment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.last_report():
            days_since_last = (date.today() - self.object.last_report().date).days
        else:
            days_since_last = None
        task_form = TaskForm()
        task_form.fields["encampment"].initial = self.object
        extra_context = {
            "visits": self.object.reports.all(),
            "days_since_last": days_since_last,
            "open_tasks": self.object.open_tasks(),
            "completed_tasks": self.object.completed_tasks(),
            "task_form": task_form,
            "url_context": f"encampment={self.object.id}",
        }
        return {**context, **extra_context}


class UserIsStaff(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CompleteTask(UserIsStaff, SingleObjectMixin, View):
    model = Task

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.mark_completed()
        return HttpResponseRedirect(task.get_absolute_url())


class CreateTask(BaseCreateView):
    form_class = TaskForm
    model = Task


class ScheduleVisitCreateView(ReportingBaseView, CreateView):
    model = ScheduledVisit
    form_class = ScheduleVisitForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        preset_encampment = self.request.GET.get("encampment")
        if preset_encampment:
            form.fields["encampment"].initial = preset_encampment
        return form


class ReportListView(ReportingBaseView, ListView):
    model = Report

    def get_queryset(self):
        return Report.objects.filter(encampment=self.kwargs["encampment"]).order_by(
            "-date"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["encampment"] = Encampment.objects.get(id=self.kwargs["encampment"])
        return context


class ReportCreateView(ReportingBaseView, CreateView):
    model = Report

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["date"].widget = date_picker()
        preset_encampment = self.request.GET.get("encampment")
        if preset_encampment:
            form.fields["encampment"].initial = preset_encampment
        return form

    fields = [
        "date",
        "encampment",
        "recorded_location",
        "performed_by",
        "supplies_delivered",
        "food_delivered",
        "occupancy",
        "talked_to",
        "assessed",
        "assessed_asymptomatic",
        "needs",
        "notes",
    ]


# API views. Maybe delete.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["encampment"]
    ordering = "date"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class EncampmentViewSet(viewsets.ModelViewSet):
    queryset = Encampment.objects.all()
    serializer_class = EncampmentSerializer
