
#Importando bibliotecas.
import requests
import pandas as pd
import pyautogui as py

contador = 0

#Lendo arquivo com os CEPS.
df = pd.read_excel(r'ceps.xlsx')

#Iterando sobre cada cep da base.
for i in range(len(df)):
    #Gera uma base provisoria a cada 10 consultas para caso haja algum erro e nao precisemos remoçar do zero
    for cep in range(len(df)):
        if contador == 10:
            endereco = df.to_excel('Enderecos.xlsx')
            contador = 0
        else:
            contador = contador + 1
    cep = df.loc[i, 'CEP']
    #consultando os ceps pela API e retornandno um JSON com os dados requisitados
    link = f'https://viacep.com.br/ws/{cep}/json/'
    requisicao = requests.get(link)
    requisicao_json = requisicao.json()

    # Tratando erro de dados ausentes dentro do Json requisitado.
    try:
        uf = requisicao_json['uf']
        cidade = requisicao_json['localidade']
        logradouro = requisicao_json['logradouro']
        bairro = requisicao_json['bairro']
        complemento = logradouro = requisicao_json['complemento']

    except KeyError:
        uf = None
        cidade = None
        logradouro = None
        bairro = None
        complemento = None

    # Criando novas colunas dentro da base de CEP
    df.loc[i, 'UF'] = uf
    df.loc[i, 'Cidade'] = cidade
    df.loc[i, 'Logradouro'] = logradouro
    df.loc[i, 'Bairro'] = bairro
    df.loc[i, 'Complemento'] = complemento

# Criando novo arquivo xlsx com o endereco completo
endreco = df.to_excel('Enderecos.xlsx', index=False)

# Mensagem de alerta informando que a base de endereços foi gerada com sucesso!!
py.alert('Base Finalizada!')



"XAU BRIGADO3"
