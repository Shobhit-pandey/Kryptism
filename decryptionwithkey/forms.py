from django import forms


class Ceasor(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt by Ceasor ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.IntegerField(initial=0,help_text="Key",required=True,min_value=0)


class Vigenere(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt by Vigenere ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class PlayFair(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt by Playfair ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class HillCipher(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt by hill cipher ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class SDes(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt  by sdes...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class Des(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt  by des...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class TripleDes(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to decrypt  by tripledes...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class Substitution(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to Encrypt  by Substitution...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key size 24",required=True)


class RailFence(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=3000, help_text='Cipher Text to Encrypt  by RailFence...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key in integer",required=True)