from django.forms import ChoiceField
from django.forms import DateInput
from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import ModelForm

from apps.reporting.models import Report
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


class ReportForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form = self

        form.fields["date"].widget = date_picker()
        form.fields["education_provided"] = ChoiceField(
            choices=[
                ("", "Choose one"),
                ("verbal", "Verbal"),
                ("flyer", "Flyer"),
                ("none", "None"),
            ],
            initial=None,
        )
        for _, field in form.fields.items():
            if isinstance(field, ChoiceField):
                field.widget.attrs["class"] = "field-select"
                field.empty_label = "Choose one"
            elif isinstance(field, IntegerField):
                field.widget.attrs["class"] = "field-number"
                field.widget.attrs["placeholder"] = "Enter a number"
            else:
                field.widget.attrs["class"] = "field-input"
                field.widget.attrs["placeholder"] = "Enter details"

        form.fields["supplies_delivered"].widget.attrs[
            "placeholder"
        ] = "Enter details or leave blank"
        form.fields["food_delivered"].widget.attrs[
            "placeholder"
        ] = "Enter details or leave blank"

    class Meta:
        model = Report
        fields = (
            "date",
            "encampment",
            "type_of_setup",
            "education_provided",
            # "recorded_location",
            "performed_by",
            "supplies_delivered",
            "food_delivered",
            "occupancy",
            "talked_to",
            "assessed",
            "assessed_asymptomatic",
            "needs",
            "notes",
        )
