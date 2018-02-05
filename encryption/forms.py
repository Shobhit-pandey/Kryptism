from django import forms


class Ceasor(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to encrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))