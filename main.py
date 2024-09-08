# Importando bibliotecas.
import requests
import pandas as pd
import pyautogui as py
import os

contador = 0

# Lendo arquivo com os CEPS.
df = pd.read_excel(r'C:\Users\eliel\OneDrive\Área de Trabalho\Busca_cep\Buscar_endereco\ceps.xlsx')

# Iterando sobre cada cep da base.
for i in range(len(df)):
    cep = df.loc[i, 'CEP']

    # Consultando os CEPs pela API e retornando um JSON com os dados requisitados.
    link = f'https://viacep.com.br/ws/{cep}/json/'
    requisicao = requests.get(link) 
    requisicao_json = requisicao.json()

    # Tratando erro de dados ausentes dentro do JSON requisitado.
    try:
        uf = requisicao_json.get('uf', '')
        cidade = requisicao_json.get('localidade', '')
        logradouro = requisicao_json.get('logradouro', '')
        bairro = requisicao_json.get('bairro', '')
        complemento = requisicao_json.get('complemento', '')
    except KeyError:
        uf, cidade, logradouro, bairro, complemento = '', '', '', '', ''

    # Criando novas colunas dentro da base de CEP.
    df.loc[i, 'UF'] = uf
    df.loc[i, 'Cidade'] = cidade
    df.loc[i, 'Logradouro'] = logradouro
    df.loc[i, 'Bairro'] = bairro
    df.loc[i, 'Complemento'] = complemento

    # Gera uma base provisória a cada 10 consultas para caso haja algum erro e não precisemos recomeçar do zero.
    if contador == 10:
        base_provisoria = df.to_excel(r'C:/Users/eliel/OneDrive/Área de Trabalho/Busca_cep/Buscar_endereco/Enderecos_parcial.xlsx', index=False)
        contador = 0
    else:
        contador += 1

# Validando e excluindo arquivo já existente
caminho_arquivo = r'C:/Users/eliel/OneDrive/Área de Trabalho/Busca_cep/Buscar_endereco/Enderecos.xlsx'

if os.path.exists(caminho_arquivo):
    os.remove(caminho_arquivo)

# Salvando o arquivo final após a última consulta.
df.to_excel(caminho_arquivo, index=False)
os.remove(r'C:\Users\eliel\OneDrive\Área de Trabalho\Busca_cep\Buscar_endereco\Enderecos_parcial.xlsx')

# Mensagem de alerta informando que a base de endereços foi gerada com sucesso!
py.alert('Base Finalizada!')