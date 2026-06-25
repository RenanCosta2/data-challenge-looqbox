import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

def get_sql_data() -> pd.DataFrame:
    # Carrega as variáveis de ambiente
    load_dotenv()
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    database = os.getenv("DATABASE")

    # Forma a string de conexão
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    # Cria o motor de conexão
    engine = create_engine(connection_string)

    # Carrega os caminhos dos arquivos SQL
    store_cad_path = os.path.join(os.path.dirname(__file__), "queries", "data_store_cad.sql")
    store_sales_path = os.path.join(os.path.dirname(__file__), "queries", "data_store_sales.sql")

    # Lê as queries de dentro dos arquivos SQL
    with open(store_cad_path, "r", encoding="utf-8") as f:
        store_cad_query = f.read()
    with open(store_sales_path, "r", encoding="utf-8") as f:
        store_sales_query = f.read()
    
    # Carrega os dados
    store_cad = pd.read_sql(store_cad_query, con=engine)
    store_sales = pd.read_sql(store_sales_query, con=engine, parse_dates=['DATE'])

    return store_cad, store_sales

def main():

    # Exemplo de execução da função
    store_cad, store_sales = get_sql_data()
    
    # Filtrando para o período especificado
    store_sales = store_sales[(store_sales['DATE'] >= '2019-10-01') & (store_sales['DATE'] <= '2019-12-31')]

    # Junção dos DataFrames a partir do STORE_CODE
    df_merged = store_cad.merge(store_sales, on='STORE_CODE', how='inner')

    # Agrupando a soma de venda e quantidade pela loja e categoria
    df_grouped = df_merged.groupby([
        'STORE_NAME',
        'BUSINESS_NAME'
    ]).agg({
        'SALES_VALUE': ['sum'],
        'SALES_QTY': ['sum']
    }).reset_index()

    # Cálculo do Ticket Médio
    df_grouped['TM'] = (df_grouped['SALES_VALUE'] / df_grouped['SALES_QTY']).round(2)

    # Mantendo e renomeando apenas as colunas necessárias
    df_result = df_grouped[['STORE_NAME', 'BUSINESS_NAME', 'TM']].rename(
		columns={
			'STORE_NAME': 'Loja',
			'BUSINESS_NAME': 'Categoria'
		}
	)

    print(df_result)

if __name__ == "__main__":
    main()