from django.http import HttpResponse
from django.shortcuts import render
from pycipher import SimpleSubstitution
# Create your views here.

from django.shortcuts import render

from encryption import pyDes
from encryption.forms import Ceasor, Vigenere, PlayFair, HillChipher, Des, SDes, TripleDes, Substitution, RailFence, \
    RSA, OTP
from DESCommon import DES, generate_keys
from DESUtil import to_binary, add_pads_if_necessary, hex_to_bin, bin_to_hex, bin_to_text
import string
import binascii
import base64
import random

def enhome(request):
    return render(request, 'en/enhome.html')


def ceasor(request):
    form = Ceasor()
    if request.method == 'POST':
        form = Ceasor(request.POST)
        if form.is_valid():
            plain_text = request.POST['input']
            key = request.POST['key']
            # print(plain_text)
            plain_text = str(plain_text)
            plain_text = plain_text.upper()
            cipher = ""
            key = int(key)
            for i in plain_text:
                cipher += (chr)((ord(i) + key - 65) % 26 + 65)
            # print(cipher)
            return render(request, 'en/ceasor.html', {'form': form,'cipher':cipher})
            # return HttpResponse("Cipher Text : "+cipher)
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
            cipher = ''
            for i in cipher_text:
                cipher += i
            return render(request, 'en/vigenere.html', {'form': form,'cipher':cipher})
            # return HttpResponse("Cipher Text : "+(str)(cipher))
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
    for e in range(int(len(message) /int(2*1.0))):
        if message[i] == message[i + 1]:
            message.insert(i + 1, 'X')
        i = i + 2

    # If it is odd digit, add an "X" at the end
    if len(message) % 2 == 1:
        message.append("X")
    # Grouping
    i = 0
    new = []
    for x in range(1, int(len(message) / (2*1.0)) + 1):
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
            return render(request, 'en/playfair.html', {'form': form,'cipher':cipher_text})
            # return HttpResponse("Cipher Text : "+str(cipher_text))
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
            plain_text = plain_text.replace(" ","")
            key = str(key)
            key = key.upper()
            plain_text = plain_text.upper()
            cipher_text = hillcipher_encrypt(plain_text, alphabet, key, is_square, chunk, stov, vtos)
            return render(request, 'en/hillcipher.html', {'form': form,'cipher':cipher_text})
            # return HttpResponse("Cipher Text : "+cipher_text)
        else:
            form = HillChipher()
    return render(request, 'en/hillcipher.html', {'form': form})


def des(request):
    form = Des()
    if request.method == 'POST':
        form = Des(request.POST)
        if form.is_valid():
            plain_text = request.POST['input']
            key = request.POST['key']
            plain_text = str(plain_text)
            key = (str)(key)
            if (len(key) < 8):
                return HttpResponse("Key must be 8 characters in length")
            cipher_text = des_encrypt(plain_text,key)
            return render(request, 'en/des.html', {'form': form,'cipher':cipher_text})
            # return HttpResponse("Encrypted text : " +(cipher_text) )
        else:
            return HttpResponse("Error in Form")
    else:
        form = Des()
    return render(request,'en/des.html',{'form':form})


def get_bits(plaintext):
    text_bits = []
    for i in plaintext:
        text_bits.extend(to_binary(ord(i)))
    return text_bits


def des_encrypt(plaintext, key_text):
    keys = generate_keys(key_text)

    text_bits = get_bits(plaintext)
    text_bits = add_pads_if_necessary(text_bits)

    final_cipher = ''
    for i in range(0, len(text_bits), 64):
        final_cipher += DES(text_bits, i, (i + 64), keys)

    # conversion of binary cipher into hex-decimal form
    hex_cipher = ''
    i = 0
    while i < len(final_cipher):
        hex_cipher += bin_to_hex(final_cipher[i:i + 4])
        i = i + 4
    return hex_cipher

rounds = 2
alphabet = string.ascii_uppercase


def bin_to_ascii_4bit(bin_string):
    h1, h2 = split_half(bin_string)
    return alphabet[bin_to_int(h1)] + alphabet[bin_to_int(h2)]


def P10(data):
    box = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    return "".join(list(map(lambda x: data[x - 1], box)))


def P8(data):
    box = [6, 3, 7, 4, 8, 5, 10, 9]
    return "".join(list(map(lambda x: data[x - 1], box)))


def P4(data):
    box = [2, 4, 3, 1]
    return "".join(list(map(lambda x: data[x - 1], box)))


def S0(data):
    row = bin_to_int(data[0] + data[3])
    col = bin_to_int(data[1] + data[2])
    box = [["01", "00", "11", "10"],
           ["11", "10", "01", "00"],
           ["00", "10", "01", "11"],
           ["11", "01", "11", "10"]
           ]

    return box[row][col]


def S1(data):
    row = bin_to_int(data[0] + data[3])
    col = bin_to_int(data[1] + data[2])
    box = [["00", "01", "10", "11"],
           ["10", "00", "01", "11"],
           ["11", "00", "01", "00"],
           ["10", "01", "00", "11"]
           ]

    return box[row][col]


def IP(data):
    box = [2, 6, 3, 1, 4, 8, 5, 7]
    return "".join(list(map(lambda x: data[x - 1], box)))


def IP_1(data):
    box = [4, 1, 3, 5, 7, 2, 8, 6]
    return "".join(list(map(lambda x: data[x - 1], box)))


def E_P(data):
    box = [4, 1, 2, 3, 2, 3, 4, 1]
    return "".join(list(map(lambda x: data[x - 1], box)))


def XOR(data, key):
    return "".join(list(map(lambda x, y: str(int(x) ^ int(y)), data, key)))


def LS(data, amount):
    return data[amount:] + data[:amount]


def SW(data):
    data1, data2 = split_half(data)
    return data2 + data1


def split_half(data):
    return data[:int(len(data) / 2)], data[int(len(data) / 2):]


def int_to_bin(data):
    return "{0:b}".format(data)


def bin_to_int(data):
    return int(data, 2)


def generate_round_keys(key, rounds):
    round_keys = []
    k_h1, k_h2 = split_half(P10(key))

    s = 0
    for i in range(1, rounds + 1):
        s += i
        h1, h2 = LS(k_h1, s), LS(k_h2, s)
        round_keys.append(P8(h1 + h2))

    return round_keys


def sdes_encrypt(data, key):
    round_keys = generate_round_keys(key, rounds)
    ip1, ip2 = split_half(IP(data))

    for i, r_key in enumerate(round_keys):
        data = E_P(ip2)
        data = XOR(data, r_key)
        d1, d2 = split_half(data)
        d1 = S0(d1)
        d2 = S1(d2)
        data = XOR(ip1, P4(d1 + d2)) + ip2

        if i != len(round_keys) - 1:
            ip1, ip2 = split_half(SW(data))
        else:
            ciphertext = IP_1(data)
    return ciphertext


def sdes(request):
    form = SDes()
    if request.method == 'POST':
        form = SDes(request.POST)
        if form.is_valid():
            # parameters
            # key = "0111111101"
            # cipher = "10100010"
            plain = request.POST['input']
            key = request.POST['key']
            plain = str(plain)
            key = str(key)
            # print("Ciphertext: {} ({})".format(cipher, bin_to_ascii_4bit(cipher)))
            # print("Key: {}".format(key))
            e = sdes_encrypt(plain, key)
            # print("Encrypted: {} ({})".format(e, bin_to_ascii_4bit(e)))
            cipher = "".format(e, bin_to_ascii_4bit(e))
            return render(request, 'en/sdes.html', {'form': form,'cipher':cipher})
            # return HttpResponse()

    else:
        form = SDes()
    return render(request, 'en/sdes.html', {'form': form})


def tripledes_encrypt(iv, key, data):
    iv = binascii.unhexlify(iv)
    key = binascii.unhexlify(key)
    k = pyDes.triple_des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data)
    d = base64.encodestring(d)
    return d


def tripledes(request):
    form = TripleDes()
    if request.method == 'POST':
        form = TripleDes(request.POST)
        if form.is_valid():
            # IV has to be 8bit long
            iv = '2132435465768797'
            plain = request.POST['input']
            key = request.POST['key']
            plain = str(plain)
            key = str(key)
            encryptdata = tripledes_encrypt(iv, key, plain)
            return render(request, 'en/tripledes.html', {'form': form,'cipher':encryptdata})
            # return HttpResponse("Encrypted Text: %s" % encryptdata)
    else:
        form = TripleDes()
    return render(request, 'en/tripledes.html', {'form': form})


def substitution(request):
    form = Substitution()
    if request.method == 'POST':
        form = Substitution(request.POST)
        if form.is_valid():
            plain = request.POST['input']
            key = request.POST['key']
            plain = str(plain)
            key = str(key)
            ss = SimpleSubstitution(key)
            cipher= ss.encipher(plain)
            return render(request, 'en/substitution.html', {'form': form,'cipher':cipher})
            # return HttpResponse("Encrypted Text: %s" % cipher)
    else:
        form = Substitution()
    return render(request, 'en/substitution.html', {'form': form})


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
            plain = request.POST['input']
            key = request.POST['key']
            plain = str(plain)
            key = int(key)
            plain = plain.replace(" ", "")
            cipher = railfence_encryptFence(plain, key, offset=0, debug=False)
            return render(request, 'en/railfence.html', {'form': form,'cipher':cipher})
            # return HttpResponse("Encrypted Text: %s" % cipher)
    else:
        form = RailFence()
    return render(request, 'en/railfence.html', {'form': form})


def rsa_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''


def rsa_multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi / e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


'''
Tests to see if a number is prime.
'''


def rsa_is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True


def rsa_generate_keypair(p, q):
    if not (rsa_is_prime(p) and rsa_is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = rsa_gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = rsa_gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = rsa_multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def rsa_encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def rsa_decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


def rsa(request):
    form = RSA()
    if request.method == 'POST':
        form = RSA(request.POST)
        if form.is_valid():
            plain = request.POST['input']
            prime1 = request.POST['prime1']
            prime2 = request.POST['prime2']
            plain = str(plain)
            prime1 = int(prime1)
            prime2 = int(prime2)
            public, private = rsa_generate_keypair(prime1, prime2)
            encrypted_msg = rsa_encrypt(public, plain)
            cipher = ''.join(map(lambda x: str(x), encrypted_msg))
            return render(request, 'en/rsa.html', {'form': form,'cipher':cipher,'public_key':public,'private':private})
            # return HttpResponse("Encrypted Text: " + str(encrypted_msg) + " public key "+ str(public) + "private key = " + str(private))
    else:
        form = RSA()
    return render(request, 'en/rsa.html', {'form': form})


def otp(request):
    if request.method == 'POST':
        form = OTP(request.POST)
        if form.is_valid():
            plain = request.POST['input']
            key = request.POST['key']
            plain = str(plain.upper())
            key = str(key.upper())
            if(len(key)<len(plain)):
                return HttpResponse("KEY is shorter than plain text")
            cipher = ''
            for i in range(0, len(plain)):
                cipher += chr(((ord(plain[i]) + ord(key[i]) - 130)%26) + 65)
            return render(request, 'en/otp.html', {'form': form,'cipher':cipher})
            # return HttpResponse("CIPHER TEXT BY OTP METHOD -  " + cipher)
        else:
            return HttpResponse("FORM NOT VALID")
    else:
        form = OTP()
    return render(request,'en/otp.html',{'form':form})