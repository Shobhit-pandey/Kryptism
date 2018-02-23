from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from decryptionwithkey.forms import Ceasor, Vigenere, PlayFair, HillCipher


def home(request):
    return render(request, 'dwk/dwkhome.html')


def ceasor(request):
    form = Ceasor()
    if request.method == 'POST':
        form = Ceasor(request.POST)
        if form.is_valid():
            cipher_text = request.POST['input']
            key = request.POST['key']
            print(cipher_text)
            cipher_text = str(cipher_text)
            plain_text = ""
            key = int(key)
            for i in cipher_text:
                plain_text += (chr)((ord(i) - key - 65) % 26 + 65)
            print(plain_text)
            return HttpResponse(plain_text)
        else:
            form = Ceasor()
    return render(request, 'dwk/ceasor.html', {'form': form})


def vigenere_decoder(code_text, source, matrix, mykey):
    control = 0
    plaintext = []

    for x, i in enumerate(code_text.upper()):
        if i not in source:
            plaintext.append(i)
            continue
        else:
            control = 0 if control % len(mykey) == 0 else control
            result = (matrix.index(i) - matrix.index(mykey[control])) % 26
            plaintext.append(source[result])
            control += 1

    return plaintext


def vigenere(request):
    import string
    form = Vigenere()
    if request.method == 'POST':
        form = Vigenere(request.POST)
        if form.is_valid():
            cipher_text = request.POST['input']
            key = request.POST['key']
            cipher_text = str(cipher_text)
            key = str(key)
            key = key.upper()
            source = string.ascii_uppercase
            shift = 1
            matrix = [source[(i + shift) % 26] for i in range(len(source))]
            plain_text = vigenere_decoder(cipher_text, source, matrix, key)
            return HttpResponse(plain_text)
        else:
            form = Vigenere()
    return render(request, 'dwk/vigenere.html', {'form': form})

def modInverse(a, m) :
    a = a % m;
    for x in range(1, m) :
        if ((a * x) % m == 1) :
            return x
    return 1

def hillcipher_decrypt(plaintext, alphabet, key, is_square, chunk, stov, vtos):
    import math
    import numpy as np
    assert isinstance(plaintext, str)
    assert isinstance(alphabet, str)
    assert isinstance(key, str)
    m = len(alphabet)  # modulo
    assert is_square(len(key))
    n = int(math.sqrt(len(key)))
    f = np.array(chunk(stov(key, alphabet), n))  # n x n matrix
    det = np.linalg.det(f)
    modin = modInverse((int)(det), 26)
    finv = np.linalg.inv(f)
    mu = np.multiply(finv, det * modin)
    mumod = np.mod(mu, 26)
    mumod = (np.rint(mumod)).astype(int)
    f = mumod
    assert len(plaintext) % n == 0

    ciphertext = ''
    for s in chunk(plaintext, n):
        x = np.array(stov(s, alphabet))
        y = np.dot(f, x) % m
        ciphertext += vtos(y.tolist(), alphabet)
    return ciphertext


def hillcipher(request):
    import math
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    stov = lambda s, alphabet: [alphabet.index(c) for c in s]
    vtos = lambda x, alphabet: ''.join([alphabet[i] for i in x])
    is_square = lambda n: int(math.sqrt(n)) ** 2 == n
    chunk = lambda s, n: [s[i:i + n] for i in range(0, len(s), n)]
    form = HillCipher()
    if request.method == 'POST':
        form = HillCipher(request.POST)
        if form.is_valid():
            cipher_text = request.POST['input']
            key = request.POST['key']
            cipher_text = str(cipher_text)
            key = str(key)
            key = key.upper()
            cipher_text = cipher_text.upper()
            plain_text = hillcipher_decrypt(cipher_text, alphabet, key, is_square, chunk, stov, vtos)
            return HttpResponse(plain_text)
        else:
            form = HillCipher()
    return render(request, 'en/hillcipher.html', {'form': form})


def playfair_matrix(key):
    matrix = []
    for e in key.upper():
        if e not in matrix:
            matrix.append(e)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for e in alphabet:
        if e not in matrix:
            matrix.append(e)

    # initialize a new list. Is there any elegant way to do that?
    matrix_group = []
    for e in range(5):
        matrix_group.append('')

    # Break it into 5*5
    matrix_group[0] = matrix[0:5]
    matrix_group[1] = matrix[5:10]
    matrix_group[2] = matrix[10:15]
    matrix_group[3] = matrix[15:20]
    matrix_group[4] = matrix[20:25]
    return matrix_group


def playfair_find_position(key_matrix, letter):
    x = y = 0
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == letter:
                x = i
                y = j

    return x, y


def playfair_cipher_to_digraphs(cipher):
    i = 0
    new = []
    for x in range(len(cipher) / 2):
        new.append(cipher[i:i + 2])
        i = i + 2
    return new


def playfair_decrypt(cipher,key):
    cipher = playfair_cipher_to_digraphs(cipher)
    key_matrix = playfair_matrix(key)
    plaintext = []
    for e in cipher:
        p1, q1 = playfair_find_position(key_matrix, e[0])
        p2, q2 = playfair_find_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            plaintext.append(key_matrix[p1][q1 - 1])
            plaintext.append(key_matrix[p1][q2 - 1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1;
            if p2 == 4:
                p2 = -1;
            plaintext.append(key_matrix[p1 - 1][q1])
            plaintext.append(key_matrix[p2 - 1][q2])
        else:
            plaintext.append(key_matrix[p1][q2])
            plaintext.append(key_matrix[p2][q1])

    for unused in range(len(plaintext)):
        if "X" in plaintext:
            plaintext.remove("X")

    output = ""
    for e in plaintext:
        output += e
    return output.lower()


def playfair(request):
    form = PlayFair()
    if request.method == 'POST':
        form = PlayFair(request.POST)
        if form.is_valid():
            cipher_text = request.POST['input']
            key = request.POST['key']
            cipher_text = str(cipher_text)
            key = str(key)
            key = key.upper()
            cipher_text=cipher_text.upper()
            message_digraph = playfair_cipher_to_digraphs(cipher_text)
            matrix = playfair_matrix(key)
            plain_text = playfair_decrypt(cipher_text, key)
            return HttpResponse(plain_text)
        else:
            form = PlayFair()
    return render(request, 'dwk/playfair.html', {'form': form})
