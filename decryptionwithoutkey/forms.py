from django import forms


class CryptoAnalysis(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt ...'}))


class Vigenere(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt ...'}))


class PlayFair(forms.Form):
    input = forms.CharField(label="Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to decrypt ...'}))


class HillCipherKnownPlainText(forms.Form):
    known_plaintext = forms.CharField(label="Known Plain Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Known Plain text ...'}))
    known_ciphertext = forms.CharField(label="Known Cipher Text", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Known Cipher Text...'}))
    enc_plaintext = forms.CharField(label="Cipher Text To cryptoanalysis", max_length=100000000000000000000000000000,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20,'placeholder': 'Cipher Text to Cryptoanalysis ...'}))