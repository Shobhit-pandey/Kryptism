from django import forms


class Ceasor(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, help_text='Plain Text to encrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.IntegerField(initial=0,help_text="Key",required=True,min_value=0)


class Vigenere(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to encrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class PlayFair(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to encrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class HillChipher(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to encrypt ...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key Should be like \"GYBNQKURP\"",required=True)


class Des(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to Encrypt  by des...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key",required=True)


class SDes(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to Encrypt  by des...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key size 10",required=True)


class TripleDes(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to Encrypt  by tripledes...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key size 24",required=True)


class Substitution(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to Encrypt  by Substitution...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key size 26",required=True)


class RailFence(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=3000, help_text='Plain Text to Encrypt  by RailFence...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    key = forms.CharField(help_text="Key in integer",required=True)