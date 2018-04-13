from django import forms


class Ceasor(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt by Ceasor ...'}))
    key = forms.IntegerField(initial=0,required=True,min_value=0,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key in integer'}))


class Vigenere(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt by Vigenere ...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key '}))


class PlayFair(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt by Playfair ...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key '}))


class HillCipher(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt by hill cipher ...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'key in "QWER"(2*2) , "NDWEINIKL"(3*3) '}))


class SDes(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt  by sdes...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key '}))


class Des(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt  by des...'}))
    key = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key '}))


class TripleDes(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt  by tripledes...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key'}))


class Substitution(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000, widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to Encrypt  by Substitution...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 40, 'rows': 1,'placeholder': 'Key size 26'}))


class RailFence(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to Encrypt  by RailFence...'}))
    key = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Key in integer'}))


class RSA(forms.Form):
    input = forms.CharField(label="Cipher Text ", max_length=100000000000000000000000000000,
                            widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': '373L, 144L, 330L, 276L, 196L, 330L, 276L, 196L, 264L, 144L, 168L, 174L, 144L, 330L, 231L, 196L, 40L, 159L, 2L, 179L, 288L, 59L'})
                            )
    key1 = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Your first value of Public Key'}))
    key2 = forms.CharField( required=True,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Your Second value of Public Key'}))