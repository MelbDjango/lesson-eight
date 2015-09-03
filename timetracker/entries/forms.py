from django import forms
from django.utils import timezone

from .models import Client, Entry, Project


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'client')


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('start', 'stop', 'project', 'description')
        labels = {'start': 'Start Time', 'stop': 'End Time'}
        help_texts = {
            'start': 'Format: 2006-10-25 14:30',
            'stop': 'Format: 2006-10-25 14:30',
            }

    def __init__(self, *args, **kwargs):
        """
        Overload ModelForm __init__ method to perform a check on submitted data
        """
        # Call superclass __init__ method first!
        super(EntryForm, self).__init__(*args, **kwargs)
        self.submit_end_now = self.data.get('submit_end_now', None)

    def clean_start(self):
        """
        Validation for start field
        """
        start = self.cleaned_data['start']
        if start >= timezone.now():
            raise forms.ValidationError('Start time must be in the past')

        # Must return the value, regardless of whether we changed it or not
        return start

    def clean_stop(self):
        """
        If the submit_end_now button was clicked set the stop time to now
        """
        stop = self.cleaned_data['stop']
        if self.submit_end_now:
            stop = timezone.now()
        return stop

    def clean(self):
        """
        This method handles the validation of the form overall and is useful
        for handling scenarios like when a field relies on another field
        """
        # Call parent's clean method to ensure any validation logic in parent
        # class is preserved
        cleaned_data = super(EntryForm, self).clean()

        # Get the start and stop values from the cleaned_data dictionary, or
        # None if the dictionary keys are missing
        start = cleaned_data.get('start', None)
        stop = cleaned_data.get('stop', None)

        if stop and start and (stop < start):
            raise forms.ValidationError('End time must come after start time')
        # No need to return anything (Django 1.7 and above)
