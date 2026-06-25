import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

def get_imdb_data():
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
    imdb_path = os.path.join(os.path.dirname(__file__), "queries", "IMDB_movies.sql")

    # Lê as queries de dentro dos arquivos SQL
    with open(imdb_path, "r", encoding="utf-8") as f:
        imdb_query = f.read()
    
    # Carrega os dados
    imdb = pd.read_sql(imdb_query, con=engine)

    return imdb

def main():
    df = get_imdb_data()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['RevenueMillions'], df['Metascore'], alpha=0.5, color='darkblue')
    
    plt.title('Relação entre Receita e Avaliação dos Filmes (IMDB)')
    plt.xlabel('Receita (em Milhões)')
    plt.ylabel('Avaliação (Metascore)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Exibe o gráfico interativo na tela
    plt.show()
    
if __name__ == "__main__":
    main()