from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from decryptionwithoutkey.forms import CryptoAnalysis


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
    form = CryptoAnalysis()
    if request.method == 'POST':
        form = CryptoAnalysis(request.POST)
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
        form = CryptoAnalysis()
    return render(request, 'dwok/ceasor.html', {'form': form})


def vigenere(request):
    if request.method == 'POST':
        form = CryptoAnalysis(request.POST)
        if form.is_valid():
            cipher = request.POST['input']
            cipher = str(cipher)
            cipher = cipher.upper()
            ic_total = []
            get = 0
            sez = 2
            for y in range(2, 26):
                list = []
                ic = []
                for x in range(0, len(cipher)):
                    if x < y:
                        list.append(cipher[x])
                    else:
                        z = x % y
                        c = list[z] + cipher[x]
                        list.remove(list[z])
                        list.insert(z, c)
                for t in list:
                    # print(t)
                    i = 0
                    for n in range(65, 91):
                        z = t.count(chr(n))
                        i += z * (z - 1)
                    try:
                        ic.append(i / (len(t) * (len(t) - 1)))
                    except:
                        return HttpResponse("Invalid INPUT...")
                ic_total.append(sum(ic) / len(ic))
                print("For " + (str)(y) + "  size  " + (str)(ic_total[y - 2]))
                if get == 0:
                    if ic_total[y - 2] > 0.065:
                        sez = y
                        get = 1

            print()
            print("size = " + str(sez))
            print()

            probabilty = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.02, 0.061, 0.07, 0.002, 0.008, 0.04, 0.024, 0.067,
                          0.075, 0.019, 0.001, 0.06, 0.063, 0.091, 0.028, 0.01, 0.024, 0.002, 0.02, 0.001]
            list = []
            key = []
            chi = 0
            for y in range(10, 11):
                for x in range(0, len(cipher)):
                    if x < y:
                        list.append(cipher[x])
                    else:
                        z = x % y
                        c = list[z] + cipher[x]
                        list.remove(list[z])
                        list.insert(z, c)
            for t in list:
                temporary_chi = []
                for y in range(0, 26):
                    plaintext = []
                    for x in range(0, len(t)):
                        z = (ord(t[x]) - 65 - y) % 26
                        if z < 0:
                            z = 26 - z
                        z += 65
                        z = chr(z)
                        plaintext.append(z)
                    xc = ''.join(map(str, plaintext))
                    i = 0
                    for n in range(65, 91):
                        z = xc.count(chr(n))
                        e = probabilty[n - 65] * len(xc)
                        chi += ((z - e) * (z - e)) / (e)
                        # print(chi)
                    temporary_chi.append(chi)
                    chi = 0
                key.append(temporary_chi.index(min(temporary_chi)))
            print(key)
            finalkey = []
            for k in key:
                finalkey.append(chr(k + 65))
            print("Key For Given Chiper is -  " + (str)(''.join(map(str, finalkey))))
            f_key = ''.join(map(str, finalkey))
            print("The Decrypted Text is --")
            original_text = []
            count = 0
            for x in cipher:
                if count == sez:
                    count = 0
                mn = ord(x) - (key[count] + 65)
                if mn < 0:
                    mn = 26 + mn
                # print(mn)
                original_text.append(chr(mn + 65))
                count += 1
            plain = ''.join(map(str, original_text))
            print(plain)
            return HttpResponse("KEY = "+ str(f_key) +" \n  "+plain)
        else:
            return HttpResponse("Form is not valid")
    else:
        form = CryptoAnalysis()
    return render(request, 'dwok/vigenere.html', {'form': form})



def substitution_cipher(request):
    from pycipher import SimpleSubstitution as SimpleSub
    import random
    import re
    from decryptionwithoutkey.ngram_score import ngram_score
    fitness = ngram_score('english_quadgrams.txt')  # load our quadgram statistics
    if request.method == 'POST':
        form = CryptoAnalysis(request.POST)
        if form.is_valid():
            cipher = request.POST['input']
            cipher = str(cipher)
            ctext = cipher.upper()
            ctext = re.sub('[^A-Z]', '', ctext.upper())
            maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            maxscore = -99e9
            parentscore, parentkey = maxscore, maxkey[:]
            print("Substitution Cipher solver, you may have to wait several iterations")
            print("for the correct result. Press ctrl+c to exit program.")
            # keep going until we are killed by the user
            i = 0
            k = 0
            best_key = ''
            plaintext = ''
            while k < 30:
                i = i + 1
                random.shuffle(parentkey)
                deciphered = SimpleSub(parentkey).decipher(ctext)
                parentscore = fitness.score(deciphered)
                count = 0
                while count < 1000:
                    a = random.randint(0, 25)
                    b = random.randint(0, 25)
                    child = parentkey[:]
                    # swap two characters in the child
                    child[a], child[b] = child[b], child[a]
                    deciphered = SimpleSub(child).decipher(ctext)
                    score = fitness.score(deciphered)
                    # if the child was better, replace the parent with it
                    if score > parentscore:
                        parentscore = score
                        parentkey = child[:]
                        count = 0
                    count = count + 1
                # keep track of best score seen so far
                k += 1
                if parentscore > maxscore:
                    maxscore, maxkey = parentscore, parentkey[:]
                    print('\nbest score so far:', maxscore, 'on iteration', i)
                    ss = SimpleSub(maxkey)
                    best_key = ''.join(maxkey)
                    plaintext = ss.decipher(ctext)
                    # print('    best key: ' + ''.join(maxkey))
                    # print('    plaintext: ' + ss.decipher(ctext))
            return HttpResponse("KEY = "+ str(best_key) +" \nPLAIN TEXT =   "+plaintext)
        else:
            return HttpResponse("Form is not valid")
    else:
        form = CryptoAnalysis()
    return render(request, 'dwok/substution.html', {'form': form})