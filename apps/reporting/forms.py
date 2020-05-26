from django.forms import HiddenInput
from django.forms import ModelForm

from apps.reporting.models import Task


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
