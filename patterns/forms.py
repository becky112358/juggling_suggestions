import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Record


class RecordForm(ModelForm):

    class Meta:
        model = Record
        fields = ['number_of_catches', 'date']

    def clean_date(self):
        data = self.cleaned_data['date']

        if data > datetime.date.today():
            raise ValidationError(_('You can do it! (And after you have, come back and log the record.)'))

        return data
