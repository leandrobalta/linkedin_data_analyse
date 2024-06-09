import pandas as pd
import mysql.connector

def load_companies():
    file_path = "csvs/companies.csv"
    df = pd.read_csv(file_path, encoding='utf-8') 

    try:
        cnx = mysql.connector.connect(
            user="unifei",
            password="unifei",
            host="localhost",
            database="explain_linkedin",
            port=3306,
        )
        cursor = cnx.cursor()

        query = """INSERT INTO company (company_id, name, description, company_size, state, country, city, zip_code, address, url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        helper = 0
        for index, row in df.iterrows():
            data_to_insert = tuple(row)
            try:
                cursor.execute(query, data_to_insert)
                cnx.commit()
                print(f"Linha {index + 1} inserida com sucesso.")
                helper += 1
                if helper == 1000:
                    break
            except mysql.connector.Error as err:
                print(f"Erro ao inserir linha {index + 1}: {err}")
                cnx.rollback()  

        cursor.execute("SELECT COUNT(*) FROM company")
        result = cursor.fetchone()
        print(f"Total de registros na tabela company: {result[0]}")

    except mysql.connector.Error as err:
        print(f"Erro de conexão MySQL: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
