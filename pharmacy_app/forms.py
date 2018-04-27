from django import forms
from .models import Medicine, MedicineUnit
from django.core.exceptions import ValidationError


class SalesForm(forms.Form):
    medicines = Medicine.objects.all()
    medicine = forms.ModelChoiceField(queryset=medicines)
    count = forms.IntegerField()

    def clean_count(self):
        print("Cleaned data: ", self.cleaned_data)
        medicine = self.cleaned_data['medicine']
        count = int(self.cleaned_data['count'])

        medicine_unit_count = MedicineUnit.objects.filter(medicine=medicine, status='a').count()

        if count > medicine_unit_count:
            self.add_error('count', ValidationError('This amount of available '
                                                    'medicines are unavailable'))
