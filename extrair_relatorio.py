from tkinter import Tk, filedialog
import requests
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2 import sql

def buscar_dados_na_api(url, token, dataPagamento, status):
    offset = 1
    
    df = pd.DataFrame()
    
 #   all_data = []

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    params = {
        'dataPagamento': dataPagamento,
        'status': status,
        'offset': offset,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        while response.status_code == 200 and data['status'] == 0:
            
            df = pd.concat([df, pd.DataFrame(data['data'])])

            print(f"Pagina: {offset} | Total de registros: {len(df)}")
            offset += 1
            params['offset'] = offset

            response = requests.get(url, headers=headers, params=params)
            data = response.json()
        
    except Exception as e:
        print(f'Erro ao buscar os dados na API: {e}')
    finally:
        return df
    
    
#Adicionar dados a tabela postGres
import psycopg2
from psycopg2 import sql

# conectar ao banco de dados
def conectar_bd():
    try:
        conexao = psycopg2.connect(
            host="jdbc:postgresql://database-rpa-dev.cduk08yuoszq.sa-east-1.rds.amazonaws.com:5432/postgres",
            database="postgres",
            user="postgres",
            password="9myOjMnAgX3OfRLKAUyP",
            encoding="utf-8"
        )
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir dados na tabela
def inserir_dados_na_tabela(dados):
    # Substitua os valores abaixo pelos dados da sua conexão e tabela
    conexao = conectar_bd()
    if conexao is not None:
        try:
            with conexao.cursor() as cursor:
                # Montando a consulta SQL de inserção
                consulta = sql.SQL("""
                    INSERT INTO  (
                        uuidLancamento, status, codigoAutenticacao, descricao,
                        numeroCpfCnpj, numeroCpfCnpjDestinatario, dataUsuarioCadastro,
                        dataVencimento, dataPagamento, codigoBarra, numeroGuia,
                        valorPrincipal, valorMulta, valorJuros,
                        valorAtualizacaoMonetaria, valorHonorariosAdvocaticios,
                        valor, uf, numeroCliente, numeroDocumento,
                        tipoDocumento, periodoApuracao, nomeContribuinte,
                        inscricaoEstadual, codigoReceita, nomeArquivo,
                        loginUsuario, statusIntegracao
                    ) VALUES (
                        %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """)
                
                # Executando a consulta SQL
                cursor.execute(consulta, dados)
                
            # Commitando as alterações no banco de dados
            conexao.commit()
            print("Dados inseridos com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir dados na tabela: {e}")
        finally:
            # Fechando a conexão
            conexao.close()

        
# Função para salvar os dados em um arquivo Excel
def salvar_em_excel(data):
    try:
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                 filetypes=[('Excel', '*.xlsx')],
                                                 initialfile=f'dados-da-api-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}',
                                                 title='Salvar dados da API'
                                                 )
        root.destroy()

        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        print(f'Arquivo salvo com sucesso em: {file_path}')
    except Exception as e:
        print(f'Erro ao salvar os dados em Excel: {e}')
        
        