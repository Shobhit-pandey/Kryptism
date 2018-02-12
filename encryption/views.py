from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

from encryption.forms import Ceasor


def enhome(request):
    return render(request, 'en/enhome.html')


def ceasor(request):
    form = Ceasor()
    if request.method == 'POST':
        form = Ceasor(request.POST)
        if form.is_valid():
            plain_text = request.POST['input']
            key = request.POST['key']
            print(plain_text)
            plain_text = str(plain_text)
            cipher = ""
            key=int(key)
            for i in plain_text:
                cipher+=(chr)((ord(i)+key-65)%26 +65)
            print(cipher)
            return HttpResponse(cipher)
        else:
            form = Ceasor()
    return render(request, 'en/ceasor.html', {'form': form})
