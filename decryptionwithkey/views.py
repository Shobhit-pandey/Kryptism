from django.http import HttpResponse
from django.shortcuts import render
from DESCommon import DES, generate_keys
from DESUtil import to_binary, add_pads_if_necessary, hex_to_bin, bin_to_hex, bin_to_text


# Create your views here.
from django.shortcuts import render
import pyDes

from DESUtil import to_binary
from decryptionwithkey.forms import Ceasor, Vigenere, PlayFair, HillCipher, SDes, Des


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
            return HttpResponse(plain_text)
        else:
            form = PlayFair()
    return render(request, 'dwk/playfair.html', {'form': form})


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
            P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
            P8 = (6, 3, 7, 4, 8, 5, 10, 9)
            P4 = (2, 4, 3, 1)
            IP = (2, 6, 3, 1, 4, 8, 5, 7)
            IPi = (4, 1, 3, 5, 7, 2, 8, 6)
            E = (4, 1, 2, 3, 2, 3, 4, 1)
            S0 = [
                [1, 0, 3, 2],
                [3, 2, 1, 0],
                [0, 2, 1, 3],
                [3, 1, 3, 2]
            ]
            S1 = [
                [0, 1, 2, 3],
                [2, 0, 1, 3],
                [3, 0, 1, 0],
                [2, 1, 0, 3]
            ]

            def permutation(perm, key):
                permutated_key = ""
                for i in perm:
                    permutated_key += key[i - 1]
                return permutated_key

            def generate_first_key(left_key, right_key):
                left_key_rot = left_key[1:] + left_key[:1]
                right_key_rot = right_key[1:] + right_key[:1]
                key_rot = left_key_rot + right_key_rot
                return permutation(P8, key_rot)

            def generate_second_key(left_key, right_key):
                left_key_rot = left_key[3:] + left_key[:3]
                right_key_rot = right_key[3:] + right_key[:3]
                key_rot = left_key_rot + right_key_rot
                return permutation(P8, key_rot)

            def F(right, subkey):
                expanded_cipher = permutation(E, right)
                xor_cipher = bin(int(expanded_cipher, 2) ^ int(subkey, 2))[2:].zfill(8)
                left_xor_cipher = xor_cipher[:4]
                right_xor_cipher = xor_cipher[4:]
                left_sbox_cipher = Sbox(left_xor_cipher, S0)
                right_sbox_cipher = Sbox(right_xor_cipher, S1)
                return permutation(P4, left_sbox_cipher + right_sbox_cipher)

            def Sbox(input, sbox):
                row = int(input[0] + input[3], 2)
                column = int(input[1] + input[2], 2)
                return bin(sbox[row][column])[2:].zfill(4)

            def f(first_half, second_half, key):
                left = int(first_half, 2) ^ int(F(second_half, key), 2)
                print
                "Fk: " + bin(left)[2:].zfill(4) + second_half
                return bin(left)[2:].zfill(4), second_half

            p10key = permutation(P10, key)
            left = p10key[:len(p10key) / 2]
            right = p10key[len(p10key) / 2:]
            first_key = generate_first_key(left, right)
            second_key = generate_second_key(left, right)
            print
            "[*] First key: " + first_key
            print
            "[*] Second key: " + second_key
            permutated_cipher = permutation(IP, cipher)
            print
            "IP: " + permutated_cipher
            first_half_cipher = permutated_cipher[:len(permutated_cipher) / 2]
            second_half_cipher = permutated_cipher[len(permutated_cipher) / 2:]
            left, right = f(first_half_cipher, second_half_cipher, second_key)
            print
            "SW: " + right + left
            left, right = f(right, left, first_key)  # switch left and right!
            print
            "IP^-1: " + permutation(IPi, left + right)
            return HttpResponse("Decrypted text : " + str(permutation(IPi, left + right)))

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
            plaintext = decrypt(cipher_text, key)
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


def decrypt(cipher, key_text):
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
