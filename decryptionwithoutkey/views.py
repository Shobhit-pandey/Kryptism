from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from decryptionwithoutkey.forms import Ceasor


def home(request):
    return render(request, 'dwok/dwokhome.html')


def ceasor(cipher_text):
    list_plaintext=[]
    for key in range(1,26):
        plain_text = ""
        for i in cipher_text:
            plain_text += (chr)((ord(i) - key - 65) % 26 + 65)
        list_plaintext.append(plain_text+"")
    return ((str)(list_plaintext[:]))


def filter_ceasor(request):
    import re
    from decryptionwithoutkey.ngram_score import ngram_score
    fitness = ngram_score('english_quadgrams.txt')  # load our quadgram statistics
    from pycipher import Caesar
    form = Ceasor()
    if request.method == 'POST':
        form = Ceasor(request.POST)
        if form.is_valid():
            cipher_text = request.POST['input']
            print(cipher_text)
            cipher_text = str(cipher_text)
            cipher_text = re.sub('[^A-Z]', '', cipher_text.upper())
            all_plain = ceasor(cipher_text)
            scores = []
            for i in range(26):
                scores.append((fitness.score(Caesar(i).decipher(cipher_text)), i))
            key = max(scores)
            return HttpResponse(Caesar(key[1]).decipher(cipher_text) +(str)("\n"+all_plain))
        else:
            return HttpResponse("Form is not valid")
    else:
        form = Ceasor()
    return render(request, 'dwok/ceasor.html', {'form': form})