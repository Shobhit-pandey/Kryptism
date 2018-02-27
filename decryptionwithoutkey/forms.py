from django import forms


class Ceasor(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))


class Vigenere(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class PlayFair(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class HillCipher(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)