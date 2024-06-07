import pandas as pd
import mysql.connector

def main():
    file_path = "csvs/companies.csv"
    df = pd.read_csv(file_path, encoding='utf-8')  # Assegurando a leitura com a codificação correta

    try:
        cnx = mysql.connector.connect(
            user="unifei",
            password="unifei",
            host="localhost",
            database="linkedin_data",
            port=3306,
            #charset='utf8mb4'  # Configurando a conexão para usar utf8mb4
        )
        cursor = cnx.cursor()

        # Preparando a query de inserção
        query = """INSERT INTO companies (company_id, name, description, company_size, state, country, city, zip_code, address, url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # Iterando sobre cada linha do DataFrame
        for index, row in df.iterrows():
            data_to_insert = tuple(row)
            try:
                cursor.execute(query, data_to_insert)
                cnx.commit()
                print(f"Linha {index + 1} inserida com sucesso.")
                if index == 1000:
                    break
            except mysql.connector.Error as err:
                print(f"Erro ao inserir linha {index + 1}: {err}")
                cnx.rollback()  # Desfazendo a transação em caso de erro

        # Verificando o número de linhas inseridas
        cursor.execute("SELECT COUNT(*) FROM companies")
        result = cursor.fetchone()
        print(f"Total de registros na tabela: {result[0]}")

    except mysql.connector.Error as err:
        print(f"Erro de conexão MySQL: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    main()
