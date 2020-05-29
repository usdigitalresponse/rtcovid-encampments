import json

from django.forms import ChoiceField
from django.forms import DateInput
from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import ModelForm
from django.forms import Select

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
    @staticmethod
    def _occupancy_field():
        ranges = [(0, 5), (6, 10), (11, 20), (21, 50), (50, None)]

        def label(r):
            if r[1] is None:
                return f"{r[0]}+"
            else:
                return f"{r[0]}-{r[1]}"

        choices = [("", "Choose one")] + [
            (json.dumps(dict(lower=r[0], upper=r[1])), label(r)) for r in ranges
        ]
        return Select(choices=choices)

    def is_valid(self):
        self.data["occupancy_0"] = json.loads(self.data.get("occupancy") or "{}").get(
            "lower"
        )
        self.data["occupancy_1"] = json.loads(self.data.get("occupancy") or "{}").get(
            "upper"
        )
        super(ReportForm, self).is_valid()

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
        form.fields["occupancy"].widget = self._occupancy_field()
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
