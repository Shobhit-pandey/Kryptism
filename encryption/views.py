from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

from encryption.forms import Ceasor, Vigenere, PlayFair, HillChipher


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
            key = int(key)
            for i in plain_text:
                cipher += (chr)((ord(i) + key - 65) % 26 + 65)
            print(cipher)
            return HttpResponse(cipher)
        else:
            form = Ceasor()
    return render(request, 'en/ceasor.html', {'form': form})


def vigenere_encoder(input_text, source, matrix, mykey):
    ciphertext = []
    control = 0

    for x, i in enumerate(input_text.upper()):
        if i not in source:
            ciphertext.append(i)
            continue
        else:
            control = 0 if control % len(mykey) == 0 else control
            result = (source.find(i) + matrix.index(mykey[control])) % 26
            ciphertext.append(matrix[result])
            control += 1

    return ciphertext


def vigenere(request):
    import string
    form = Vigenere()
    if request.method == 'POST':
        form = Vigenere(request.POST)
        if form.is_valid():
            plain_text = request.POST['input']
            key = request.POST['key']
            plain_text = str(plain_text)
            key = str(key)
            key = key.upper()
            source = string.ascii_uppercase
            shift = 1
            matrix = [source[(i + shift) % 26] for i in range(len(source))]
            cipher_text = vigenere_encoder(plain_text, source, matrix, key)
            return HttpResponse(cipher_text)
        else:
            form = Vigenere()
    return render(request, 'en/vigenere.html', {'form': form})


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


def playfair_message_to_digraphs(message_original):
    message = []
    for e in message_original:
        message.append(e)

    # Delet space
    for unused in range(len(message)):
        if " " in message:
            message.remove(" ")

    # If both letters are the same, add an "X" after the first letter.
    i = 0
    for e in range(len(message) / 2):
        if message[i] == message[i + 1]:
            message.insert(i + 1, 'X')
        i = i + 2

    # If it is odd digit, add an "X" at the end
    if len(message) % 2 == 1:
        message.append("X")
    # Grouping
    i = 0
    new = []
    for x in xrange(1, len(message) / 2 + 1):
        new.append(message[i:i + 2])
        i = i + 2
    return new


def playfair_find_position(key_matrix, letter):
    x = y = 0
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == letter:
                x = i
                y = j

    return x, y


def playfair_encrypt(message, key):
    message = playfair_message_to_digraphs(message)
    key_matrix = playfair_matrix(key)
    cipher = []
    for e in message:
        p1, q1 = playfair_find_position(key_matrix, e[0])
        p2, q2 = playfair_find_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            cipher.append(key_matrix[p1][q1 + 1])
            cipher.append(key_matrix[p1][q2 + 1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1;
            if p2 == 4:
                p2 = -1;
            cipher.append(key_matrix[p1 + 1][q1])
            cipher.append(key_matrix[p2 + 1][q2])
        else:
            cipher.append(key_matrix[p1][q2])
            cipher.append(key_matrix[p2][q1])
    return cipher


def playfair(request):
    form = PlayFair()
    if request.method == 'POST':
        form = PlayFair(request.POST)
        if form.is_valid():
            plain_text = request.POST['input']
            key = request.POST['key']
            plain_text = str(plain_text)
            key = str(key)
            key = key.upper()
            plain_text = plain_text.upper()
            message_digraph = playfair_message_to_digraphs(plain_text)
            matrix = playfair_matrix(key)
            cipher_text = playfair_encrypt(plain_text, key)
            return HttpResponse(cipher_text)
        else:
            form = PlayFair()
    return render(request, 'en/playfair.html', {'form': form})


def hillcipher_encrypt(plaintext, alphabet, key, is_square, chunk, stov, vtos):
    import math
    import numpy as np
    assert isinstance(plaintext, str)
    assert isinstance(alphabet, str)
    assert isinstance(key, str)
    m = len(alphabet)  # modulo
    assert is_square(len(key))
    n = int(math.sqrt(len(key)))
    f = np.array(chunk(stov(key, alphabet), n))  # n x n matrix
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
    form = HillChipher()
    if request.method == 'POST':
        form = HillChipher(request.POST)
        if form.is_valid():
            plain_text = request.POST['input']
            key = request.POST['key']
            plain_text = str(plain_text)
            key = str(key)
            key = key.upper()
            plain_text = plain_text.upper()
            cipher_text = hillcipher_encrypt(plain_text, alphabet, key, is_square, chunk, stov, vtos)
            return HttpResponse(cipher_text)
        else:
            form = HillChipher()
    return render(request, 'en/hillcipher.html', {'form': form})
