import os
import sys

def leitor(numero): # Lê do arquivo de entrada
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

def escrita(str_bit, nome_arquivo_saida): # Escreve no arquivo de saída
    global bit_stream
    bit_stream += str_bit

    while len(bit_stream) > 8:
        str_byte = bit_stream[:8]
        bit_stream = bit_stream[8:]
        chr_int_str_byte = chr(int(str_byte, 2))
        nome_arquivo_saida.write(bytes(chr_int_str_byte))

def fibonacci_encode(numero):
    saida = ""
    if numero >= 1: # Início da sequência fibonacci
        pri_aux = 1
        seg_aux = 1
        prox_num = pri_aux + seg_aux # Pega o próximo número da sequência
        lista_numeros = [seg_aux] # Cria a lista
        saida = "1"

        while numero >= prox_num: # Realiza a sequência
            lista_numeros.append(prox_num) # Adiciona o próximo número da sequência
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

if entrada == 'encode': # Se for escolhido o encode no pipeline
    lista_frequencia = [0] * 256
    for i_byte in array_de_bytes: # Calcula a frequência de cada byte no arquivo
        lista_frequencia[i_byte] += 1

    lista = []
    for i_byte in range(256): # Cria uma tupla contendo os valores de frequencia, valor do byte e a string do bit codificada
        if lista_frequencia[i_byte] > 0:
            lista.append((lista_frequencia[i_byte], i_byte, ''))

    lista = sorted(lista, key=lambda tupla: tupla[0], reverse = True) # Ordena pela frequência, em ordem descendente

    for b in range(len(lista)): # Bit codificado recebe valor do byte
        lista[b] = (lista[b][0], lista[b][1], fibonacci_encode(b + 1))

    bit_stream = ''
    chr_len_tuple = chr(len(lista) - 1)

    arquivo_output = open(nome_arquivo_saida, 'wb')
    arquivo_output.write(bytes(chr_len_tuple)) # Escreve a quantidade de bytes

    for (freq, valor_do_byte, bit_str_encoding) in lista:
      chr_valor_byte = chr(valor_do_byte)
      arquivo_output.write(bytes(chr_valor_byte)) # Escreve o valor do byte no arquivo

    str_bit = bin(tamanho_arquivo - 1) # Retorna o tamanho do arquivo em binário
    str_bit = str_bit[2:] # Remove o início do arquivo, pois não é necessário
    str_bit = '0' * (32 - len(str_bit)) + str_bit
    escrita(str_bit, arquivo_output)

    # Dicionário que contém o valor do byte e a string do bit codificada
    dic = dict([(tupla[1], tupla[2]) for tupla in lista])

    # Escreve os dados codificados
    for b in array_de_bytes:
        escrita(dic[b], arquivo_output)

    escrita('0' * 8, arquivo_output)
    arquivo_output.close()

elif entrada == 'decode': # Se for escolhido o decode no pipeline
    posicao_bit = 0
    n = int(leitor(8), 2) + 1
    dic = dict()

    for i in range(n):
        valor_do_byte = int(leitor(8), 2)
        bit_str_encoding = fibonacci_encode(i + 1)
        dic[bit_str_encoding] = valor_do_byte

    bytes_num = long(leitor(32), 2) + 1

    arquivo_output = open(nome_arquivo_saida, 'wb') # Abre o arquivo de saída para escrita

    for b in range(bytes_num): # Vai lendo de bit em bit até que ache um padrão para decodificar
        bit_str_encoding = ''
        while True:
            bit_str_encoding += leitor(1)
            if bit_str_encoding.endswith('11') and bit_str_encoding in dic:
                valor_do_byte = dic[bit_str_encoding]
                chr_valor_do_byte = chr(valor_do_byte)
                arquivo_output.write(bytes(chr_valor_do_byte))
                break

    arquivo_output.close()
