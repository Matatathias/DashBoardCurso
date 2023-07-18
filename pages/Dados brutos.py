# BIBLIOTECAS
from datetime import datetime as dt
import streamlit as st
import pandas as pd
import requests
import time

# CACHEAR OS DADOS AO ABRIR A PAQUINA
@st.cache_data

# FUNCOES
## CONVERTER DATAFRAME PARA ARQUIVO
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')

## MSG DE SUCESSO
def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon='✅')
    sucesso.empty()

# TITULO DA PAGINA
st.title('DADOS BRUTOS')

# LEITURA DOS DADOS USANDO REQUESTS PARA ACESSAR UM ARQUIVOS JSON E PASSAR PARA DATAFRAME PANDAS
url = 'https://labdados.com/produtos'

## REQUISICAO DA URL
response = requests.get(url)

## CRIACAO DE DATAFRAME APARTIR DO JSON OBTIDO NO RETORNO DA URL
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

# CRIANDO MENU SUSPENSO COM EXPANDER 
with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

# CRIANDO MENU LATERAL DE FILTROS COM MENU EXPANDER
## TITULO DO MENU EXPANDER DE FILTROS
st.sidebar.title('Filtros')

## CRIAR FILTRO DE NOME DO PRODUTO
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())

## CRIAR FILTRO DE CATEGOIRIA DO PRODUTO
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

## CRIAR FILTRO DE PRECO
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))

## CRIAR FILTRO DE VALOR DE FRETE
with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0,250, (0,250))

## CRIA FILTRO DE DATA DA COMPRA
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

## CRIAR FILTRO DE VENDEDOR
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())

## CRIAR FILTRO DE LOCAL DA COMPRA
with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())

## CRIAR FILTRO DE AVALIACAO DA COMPRA
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra',1,5, value = (1,5))

## CRIAR FILTRO DE TIPO DE PAGAMENTO
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

## CRIAR FILTRO DE QUANTIDADE DE PARCELAS
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))

# APLICANDO OS FILTROS 
## CRIA A QUERY PARA OS FILTROS
query = '''
    Produto in @produtos and \
    `Categoria do Produto` in @categoria and \
    @preco[0] <= Preço <= @preco[1] and \
    @frete[0] <= Frete <= @frete[1] and \
    @data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
    Vendedor in @vendedores and \
    `Local da compra` in @local_compra and \
    @avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
    `Tipo de pagamento` in @tipo_pagamento and \
    @qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

## APLICA OS FILTROS DA QUERY
dados_filtrado = dados.query(query)

## APLICA SELECAO DE COLUNAS
dados_filtrado = dados_filtrado[colunas]

# APRESENTAR O DATAFRAME
st.dataframe(dados_filtrado)

# CRIA UM TEXTO FALANDO O NUMERO DE LINHAS E COLUNAS
st.markdown(f'A tabela possui :blue[{dados_filtrado.shape[0]}] linhas e :blue[{dados_filtrado.shape[1]}] colunas')

# BOTAO DE DOWNLOAD
st.markdown('Escreva o nome do arquivo')
coluna1, coluna2 = st.columns(2)

with coluna1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o download da tabela em csv', data=converte_csv(dados_filtrado), file_name=nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)
