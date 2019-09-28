import os
import sys

def leitor(numero):
    global array_de_bytes
    global posicao_bit
    str_bit = ''

    for i in range(numero):
        posicao_bit_no_byte = 7 - (posicao_bit % 8)
        posicao_byte = int(posicao_bit / 8)
        byte_valor = array_de_bytes[posicao_byte]
        valor_bit = int(byte_valor / (2 ** posicao_bit_no_byte)) % 2
        str_bit += str(valor_bit)
        posicao_bit += 1

    return str_bit

def escrita(str_bit, nome_arquivo_saida):
    global bit_stream
    bit_stream += str_bit

    while len(bit_stream) > 8:
        str_byte = bit_stream[:8]
        bit_stream = bit_stream[8:]
        chr_int_str_byte = chr(int(str_byte, 2))
        nome_arquivo_saida.write(bytes(chr_int_str_byte))

def fibonacci_encode(numero):
    saida = ""
    if numero >= 1:
        pri_aux = 1
        seg_aux = 1
        prox_num = pri_aux + seg_aux
        lista_numeros = [seg_aux]
        saida = "1"

        while numero >= prox_num:
            lista_numeros.append(prox_num)
            pri_aux = seg_aux
            seg_aux = prox_num
            prox_num = pri_aux + seg_aux

        for numero_fibonacci in reversed(lista_numeros):
            if numero >= numero_fibonacci:
                numero = numero - numero_fibonacci
                saida = "1" + saida
            else:
                saida = "0" + saida

    return saida

if len(sys.argv) != 4:
    print('Para rodar o programa: python fibonacci.py [encode / decode] nomeArquivoEntrada nomeArquivoSaida')
    sys.exit()

entrada = sys.argv[1]
nome_arquivo_entrada = sys.argv[2]
nome_arquivo_saida = sys.argv[3]

tamanho_arquivo = os.path.getsize(nome_arquivo_entrada)
arquivo_input = open(nome_arquivo_entrada, 'rb')
array_de_bytes = bytearray(arquivo_input.read(tamanho_arquivo))
arquivo_input.close()
tamanho_arquivo = len(array_de_bytes)

if entrada == 'encode':
    lista_frequencia = [0] * 256

    for b in array_de_bytes:
        lista_frequencia[b] += 1

    lista = []

    for b in range(256):
        if lista_frequencia[b] > 0:
            lista.append((lista_frequencia[b], b, ''))

    lista = sorted(lista, key=lambda tupla: tupla[0], reverse = True)

    for b in range(len(lista)):
        lista[b] = (lista[b][0], lista[b][1], fibonacci_encode(b + 1))

    bit_stream = ''
    chr_len_tuple = chr(len(lista) - 1)

    arquivo_output = open(nome_arquivo_saida, 'wb')
    arquivo_output.write(bytes(chr_len_tuple))

    for (freq, valor_do_byte, bit_str_encoding) in lista:
      chr_valor_byte = chr(valor_do_byte)
      arquivo_output.write(bytes(chr_valor_byte))

    str_bit = bin(tamanho_arquivo - 1)
    str_bit = str_bit[2:]
    str_bit = '0' * (32 - len(str_bit)) + str_bit
    escrita(str_bit, arquivo_output)

    dic = dict([(tupla[1], tupla[2]) for tupla in lista])

    for b in array_de_bytes:
        escrita(dic[b], arquivo_output)

    escrita('0' * 8, arquivo_output)
    arquivo_output.close()

elif entrada == 'decode':
    posicao_bit = 0
    n = int(leitor(8), 2) + 1
    dic = dict()

    for i in range(n):
        valor_do_byte = int(leitor(8), 2)
        bit_str_encoding = fibonacci_encode(i + 1)
        dic[bit_str_encoding] = valor_do_byte

    bytes_num = long(leitor(32), 2) + 1

    arquivo_output = open(nome_arquivo_saida, 'wb')

    for b in range(bytes_num):
        bit_str_encoding = ''

        while True:
            bit_str_encoding += leitor(1)

            if bit_str_encoding.endswith('11') and bit_str_encoding in dic:
                valor_do_byte = dic[bit_str_encoding]
                chr_valor_do_byte = chr(valor_do_byte)
                arquivo_output.write(bytes(chr_valor_do_byte))
                break

    arquivo_output.close()
