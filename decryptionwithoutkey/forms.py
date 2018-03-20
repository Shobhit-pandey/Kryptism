from django import forms


class CryptoAnalysis(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))


class Vigenere(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))


class PlayFair(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))


class HillCipher(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))