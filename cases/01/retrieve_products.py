import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd


def retrieve_data(product_code: int, store_code: int, date: list[str]) -> pd.DataFrame:
    """
    Recupera os dados de vendas de produtos para um produto e uma loja específicos, em um período de tempo especificado.

    Args:
        product_code (int): Código do produto filtrado.
        store_code (int): Código da loja filtrada.
        date (list[str]): Lista contendo a data inicial e a data final.

    Returns:
        pd.DataFrame: Um DataFrame contendo as vendas dos produtos para o produto e a loja especificados, no período passado.
    """


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

    # Leitura dos arquivos SQL e aplicação das variáveis
    query_path = os.path.join(os.path.dirname(__file__), "queries", "get_product.sql")
    try:
        with open(query_path, "r", encoding="utf-8") as f:
            sql_template = f.read()

        sql_query = sql_template.format(
            product_code=product_code,
            store_code=store_code,
            start_date=date[0],
            end_date=date[1]
            )

    except Exception as e:
        print(f'Error: {e}')

    df = pd.read_sql(sql_query, con=engine)

    return df


def main():

    # Exemplo de execução da função
    df = retrieve_data(18, 1, ['2019-01-01', '2019-01-31'])
    print(df)

if __name__ == "__main__":
    main()