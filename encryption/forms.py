from django import forms


class Ceasor(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, help_text='',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by Ceasor...'}))
    key = forms.IntegerField(initial=0,required=True,min_value=0,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key'}))


class Vigenere(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by Vigenere...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key'}))


class PlayFair(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by Play Fair...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key'}))


class HillChipher(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by Hill Cipher...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key Should be like \"GYBNQKURP\"'}))


class Des(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by DES...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key'}))


class SDes(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by SDES...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key size 10'}))


class TripleDes(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by Triple DES...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key size 24'}))


class Substitution(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by Substitution...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 40, 'rows': 1,'placeholder': 'Key size 26'}))


class RailFence(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by RailFence...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key in integer'}))


class RSA(forms.Form):
    input = forms.CharField(label="Plain Text", max_length=100000000000000000000000000000, help_text='PLain Text to Encrypt  by RSA...',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Plain Text to encrypt by RSA...'}))
    prime1 = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Your 1st prime number (any prime number)'}))
    prime2 = forms.CharField(help_text="", required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Your 2nd prime Key (any prime number but different from private)'}))