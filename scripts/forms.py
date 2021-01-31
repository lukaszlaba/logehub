from django import forms

class Value_form(forms.Form):
    value = forms.CharField(label='k = ', max_length=100)

class Choice_form(forms.Form):
    c =[("1.12", "1.12"), ("2.12", "2.12")]
    value = forms.ChoiceField(choices=c, label="k = ")