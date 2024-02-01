import pandas as pd
from extrair_relatorio import buscar_dados_na_api, salvar_em_excel, inserir_dados_na_tabela

if __name__ == "__main__":

    # Realiza a busca na API e salva os dados em um arquivo Excel
    url = 'https://app.bancoutil.com.br/api/v1/payment' # URL da API
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcHAuYmFuY291dGlsLmNvbS5iciIsImF1ZCI6ImFwcC5iYW5jb3V0aWwuY29tLmJyIiwic3ViIjoiQVBJIiwiZXhwIjoiMzI1MDM2MDQ0MDAiLCJpZENsaWVudGUiOiIxNTciLCJpZENvbnRhIjoiMTY4Iiwic2lzdGVtYU9yaWdlbSI6IkFQSSBMT0dHSSIsImRhdGFDcmlhY2FvVG9rZW4iOiIyMDIzLTA0LTAzIn0.amsF7kjpcUPM-YgjWFmkiyTd7KARWT_IuiF-Nxqt-00'
        
    day = 1
    month = '01'
    year = '2023'
        
    df = pd.DataFrame()
    
    while day <= 31:
        dataPagamento = f'{year}-{month}-{day}'
        print("Dados do dia: ", dataPagamento) 
        dados_da_api = buscar_dados_na_api( url, token, dataPagamento=dataPagamento, status='PAGO')
        df = pd.concat([df, pd.DataFrame(dados_da_api)])
        day += 1
        
    salvar_em_excel(df)    