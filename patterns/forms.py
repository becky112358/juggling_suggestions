import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Goal, Record


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = []


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['number_of_catches', 'date']

    def clean_date(self):
        data = self.cleaned_data['date']

        if data > datetime.date.today():
            raise ValidationError(_('You can do it! (And after you have, come back and log the record.)'))

        return data


# TODO Make forms extendable for indefinite numbers of jugglers
class RecordFormTwoJugglers(RecordForm):
    def __init__(self, *args, **kwargs):
        other_users = kwargs.pop('other_users')
        super(RecordFormTwoJugglers, self).__init__(*args, **kwargs)
        self.fields['user2'].queryset = other_users

    class Meta:
        model = Record
        fields = ['number_of_catches', 'date', 'user2']
