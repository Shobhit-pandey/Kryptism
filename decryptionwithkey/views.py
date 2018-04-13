from django.http import HttpResponse
from django.shortcuts import render
from DESCommon import DES, generate_keys
from DESUtil import to_binary, add_pads_if_necessary, hex_to_bin, bin_to_hex, bin_to_text
from pycipher import SimpleSubstitution
# Create your views here.
from django.shortcuts import render
import pyDes

from DESUtil import to_binary
from decryptionwithkey.forms import Ceasor, Vigenere, PlayFair, HillCipher, SDes, Des, TripleDes, Substitution, \
    RailFence, RSA
import string
import binascii
import base64
import random
import encryption.pyDes

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
            cipher_text = cipher_text.upper()
            plain_text = ""
            key = int(key)
            for i in cipher_text:
                plain_text += (chr)((ord(i) - key - 65) % 26 + 65)
            print(plain_text)
            return HttpResponse("Plain Text : "+plain_text)
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
            return HttpResponse("Plain Text : "+plain_text)
        else:
            form = Vigenere()
    return render(request, 'dwk/vigenere.html', {'form': form})


def modInverse(a, m):
    a = a % m;
    for x in range(1, m):
        if ((a * x) % m == 1):
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
            return HttpResponse("Plain Text : "+plain_text)
        else:
            form = HillCipher()
    return render(request, 'dwk/hillcipher.html', {'form': form})


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


def playfair_decrypt(cipher, key):
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
            cipher_text = cipher_text.upper()
            message_digraph = playfair_cipher_to_digraphs(cipher_text)
            matrix = playfair_matrix(key)
            plain_text = playfair_decrypt(cipher_text, key)
            return HttpResponse("PLAIN TEXT : "+plain_text)
        else:
            return HttpResponse("Form not valid")
    else:
        form = PlayFair()
    return render(request, 'dwk/playfair.html', {'form': form})


rounds = 2
alphabet = string.ascii_uppercase


def sdes_bin_to_ascii_4bit(bin_string):
    h1, h2 = sdes_split_half(bin_string)
    return alphabet[sdes_bin_to_int(h1)] + alphabet[sdes_bin_to_int(h2)]


def sdes_P10(data):
    box = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    return "".join(list(map(lambda x: data[x - 1], box)))


def sdes_P8(data):
    box = [6, 3, 7, 4, 8, 5, 10, 9]
    return "".join(list(map(lambda x: data[x - 1], box)))


def sdes_P4(data):
    box = [2, 4, 3, 1]
    return "".join(list(map(lambda x: data[x - 1], box)))


def sdes_S0(data):
    row = sdes_bin_to_int(data[0] + data[3])
    col = sdes_bin_to_int(data[1] + data[2])
    box = [["01", "00", "11", "10"],
           ["11", "10", "01", "00"],
           ["00", "10", "01", "11"],
           ["11", "01", "11", "10"]
           ]

    return box[row][col]


def sdes_S1(data):
    row = sdes_bin_to_int(data[0] + data[3])
    col = sdes_bin_to_int(data[1] + data[2])
    box = [["00", "01", "10", "11"],
           ["10", "00", "01", "11"],
           ["11", "00", "01", "00"],
           ["10", "01", "00", "11"]
           ]

    return box[row][col]


def sdes_IP(data):
    box = [2, 6, 3, 1, 4, 8, 5, 7]
    return "".join(list(map(lambda x: data[x - 1], box)))


def sdes_IP_1(data):
    box = [4, 1, 3, 5, 7, 2, 8, 6]
    return "".join(list(map(lambda x: data[x - 1], box)))


def sdes_E_P(data):
    box = [4, 1, 2, 3, 2, 3, 4, 1]
    return "".join(list(map(lambda x: data[x - 1], box)))


def sdes_XOR(data, key):
    return "".join(list(map(lambda x, y: str(int(x) ^ int(y)), data, key)))


def sdes_LS(data, amount):
    return data[amount:] + data[:amount]


def sdes_SW(data):
    data1, data2 = sdes_split_half(data)
    return data2 + data1


def sdes_split_half(data):
    return data[:int(len(data) / 2)], data[int(len(data) / 2):]


def sdes_int_to_bin(data):
    return "{0:b}".format(data)


def sdes_bin_to_int(data):
    return int(data, 2)


def sdes_generate_round_keys(key, rounds):
    round_keys = []
    k_h1, k_h2 = sdes_split_half(sdes_P10(key))

    s = 0
    for i in range(1, rounds + 1):
        s += i
        h1, h2 = sdes_LS(k_h1, s), sdes_LS(k_h2, s)
        round_keys.append(sdes_P8(h1 + h2))

    return round_keys


def sdes_decrypt(data, key, comments=False):
    round_keys = list(reversed(sdes_generate_round_keys(key, rounds)))
    ip1, ip2 = sdes_split_half(sdes_IP(data))
    if comments:
        print("IP: {}".format(ip1 + ip2))

    for i, r_key in enumerate(round_keys):
        data = sdes_E_P(ip2)
        data = sdes_XOR(data, r_key)
        d1, d2 = sdes_split_half(data)
        d1 = sdes_S0(d1)
        d2 = sdes_S1(d2)
        data = sdes_XOR(ip1, sdes_P4(d1 + d2)) + ip2
        if comments and i == 0:
            print("First Fk: {}".format(data))
        elif comments and i == 1:
            print("Second Fk: {}".format(data))

        if i != len(round_keys) - 1:
            ip1, ip2 = sdes_split_half(sdes_SW(data))
            if comments:
                print("SW: {}".format(ip1 + ip2))
        else:
            plaintext = sdes_IP_1(data)
            if comments:
                print("IP-1: {}".format(plaintext))

    return plaintext


def sdes(request):
    form = SDes()
    if request.method == 'POST':
        form = SDes(request.POST)
        if form.is_valid():
            # parameters
            # key = "0111111101"
            # cipher = "10100010"
            cipher = request.POST['input']
            key = request.POST['key']
            cipher = str(cipher)
            key = str(key)
            # print("Ciphertext: {} ({})".format(cipher, bin_to_ascii_4bit(cipher)))
            # print("Key: {}".format(key))
            d = sdes_decrypt(cipher, key, comments=True)
            print("Decrypted: {} ({})".format(d, sdes_bin_to_ascii_4bit(d)))
            return HttpResponse("Decrypted: {} ({})".format(d, sdes_bin_to_ascii_4bit(d)))

        else:
            form = SDes()
    return render(request, 'dwk/sdes.html', {'form': form})


def des(request):
    form = Des()
    if request.method == 'POST':
        form = Des(request.POST)
        if form.is_valid():
            cipher_text = request.POST['input']
            key = request.POST['key']
            cipher_text = str(cipher_text)
            key = (str)(key)
            if (len(key) < 8):
                return HttpResponse("Key must be 8 characters in length")
            plaintext = des_decrypt(cipher_text, key)
            return HttpResponse("Decrypted text : " + (plaintext))
        else:
            return HttpResponse("Error in Form")
    else:
        form = Des()
    return render(request, 'dwk/des.html', {'form': form})


def get_bits(plaintext):
    text_bits = []
    for i in plaintext:
        text_bits.extend(to_binary(ord(i)))
    return text_bits


def des_decrypt(cipher, key_text):
    keys = generate_keys(key_text)

    text_bits = []
    ciphertext = ''
    for i in cipher:
        # conversion of hex-decimal form to binary form
        ciphertext += hex_to_bin(i)
    for i in ciphertext:
        text_bits.append(int(i))

    text_bits = add_pads_if_necessary(text_bits)
    keys.reverse()
    bin_mess = ''
    for i in range(0, len(text_bits), 64):
        bin_mess += DES(text_bits, i, (i + 64), keys)

    i = 0
    text_mess = ''
    while i < len(bin_mess):
        text_mess += bin_to_text(bin_mess[i:i + 8])
        i = i + 8
    return text_mess.rstrip('\x00')


def tripledes_decrypt(iv, key, data):
    iv = binascii.unhexlify(iv)
    key = binascii.unhexlify(key)
    k = pyDes.triple_des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    data = base64.decodestring(data)
    d = k.decrypt(data)
    return d


def tripledes(request):
    form = TripleDes()
    if request.method == 'POST':
        form = TripleDes(request.POST)
        if form.is_valid():
            # IV has to be 8bit long
            iv = '2132435465768797'
            cipher = request.POST['input']
            key = request.POST['key']
            plain = str(cipher)
            key = str(key)
            decryptdata = tripledes_decrypt(iv, key, cipher)
            return HttpResponse("Plain Text: %s" % decryptdata)
    else:
        form = TripleDes()
    return render(request, 'dwk/tripledes.html', {'form': form})


def substitution(request):
    form = Substitution()
    if request.method == 'POST':
        form = Substitution(request.POST)
        if form.is_valid():
            cipher = request.POST['input']
            key = request.POST['key']
            cipher = str(cipher)
            key = str(key)
            ss = SimpleSubstitution(key)
            plain= ss.decipher(cipher)
            return HttpResponse("Plain Text: %s" % plain)
    else:
        form = Substitution()
    return render(request, 'dwk/substitution.html', {'form': form})


def railfence_printFence(fence):
    for rail in range(len(fence)):
        print
        ''.join(fence[rail])


def railfence_encryptFence(plain, rails, offset=0, debug=False):
    cipher = ''

    # offset
    plain = '#' * offset + plain

    length = len(plain)
    fence = [['#'] * length for _ in range(rails)]

    # build fence
    rail = 0
    for x in range(length):
        fence[rail][x] = plain[x]
        if rail >= rails - 1:
            dr = -1
        elif rail <= 0:
            dr = 1
        rail += dr

    # print pretty fence
    if debug:
        railfence_printFence(fence)

    # read fence
    for rail in range(rails):
        for x in range(length):
            if fence[rail][x] != '#':
                cipher += fence[rail][x]
    return cipher


def railfence_decryptFence(cipher, rails, offset=0, debug=False):
    plain = ''

    # offset
    if offset:
        t = railfence_encryptFence('o' * offset + 'x' * len(cipher), rails)
        for i in range(len(t)):
            if (t[i] == 'o'):
                cipher = cipher[:i] + '#' + cipher[i:]

    length = len(cipher)
    fence = [['#'] * length for _ in range(rails)]

    # build fence
    i = 0
    for rail in range(rails):
        p = (rail != (rails - 1))
        x = rail
        while (x < length and i < length):
            fence[rail][x] = cipher[i]
            if p:
                x += 2 * (rails - rail - 1)
            else:
                x += 2 * rail
            if (rail != 0) and (rail != (rails - 1)):
                p = not p
            i += 1

    # print pretty fence
    if debug:
        railfence_printFence(fence)

    # read fence
    for i in range(length):
        for rail in range(rails):
            if fence[rail][i] != '#':
                plain += fence[rail][i]
    return plain


def railfence(request):
    form = RailFence()
    if request.method == 'POST':
        form = RailFence(request.POST)
        if form.is_valid():
            cipher = request.POST['input']
            key = request.POST['key']
            cipher = str(cipher)
            key = int(key)
            plain = railfence_decryptFence(cipher, key, offset=0, debug=True)
            return HttpResponse("Decrypyed Text: %s" % plain)
    else:
        form = RailFence()
    return render(request, 'dwk/railfence.html', {'form': form})


def rsa(request):
    form = RSA()
    if request.method == 'POST':
        form = RSA(request.POST)
        if form.is_valid():
            cipher = request.POST['input']
            key1 = request.POST['key1']
            key2 = request.POST['key2']
            cipher = (cipher)
            # cipher = [373L, 144L, 330L, 276L, 196L, 330L, 276L, 196L, 264L, 144L, 168L, 174L, 144L, 330L, 231L, 196L,
            #           40L, 159L, 2L, 179L, 288L, 59L]
            key1 = int(key1)
            key2 = int(key2)
            cipher = cipher.replace(",","")
            cipher = cipher.replace("L", "")
            cipher=cipher.split()
            new_cipher = []
            for i in cipher:
                new_cipher.append(int(i))
            print(new_cipher)
            plain = [chr((char ** key1) % key2) for char in new_cipher]
            print(plain)
            # cipher = [373L, 144L, 330L, 276L, 196L, 330L, 276L, 196L, 264L, 144L, 168L, 174L, 144L, 330L, 231L, 196L, 40L, 159L, 2L, 179L, 288L, 59L]
            # key1 = 259
            # key2 = 391
            return HttpResponse("Plain Text: " + ''.join(plain) )
    else:
        form = RSA()
    return render(request, 'dwk/rsa.html', {'form': form})