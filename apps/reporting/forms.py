from django.forms import DateInput
from django.forms import HiddenInput
from django.forms import ModelForm

from apps.reporting.models import ScheduledVisit
from apps.reporting.models import Task


def date_picker():
    return DateInput(
        attrs={"type": "date", "class": "field-date", "placeholder": "YYYY-MM-DD"}
    )


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = "Task title"
        self.fields["details"].widget.attrs["placeholder"] = "Task details"
        self.fields["title"].label = False
        self.fields["details"].label = False

    class Meta:
        model = Task
        fields = ("title", "details", "encampment")
        widgets = {
            "encampment": HiddenInput(),
        }


class ScheduleVisitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["encampment"].widget.attrs["class"] = "field-select"
        self.fields["organization"].widget.attrs["class"] = "field-select"

    class Meta:
        model = ScheduledVisit
        fields = ("encampment", "date", "organization")
        widgets = {"date": date_picker()}
