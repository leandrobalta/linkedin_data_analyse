import pandas as pd
import mysql.connector

def load_profiles():
    file_path = "csvs/profiles.csv"
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

        query = """INSERT INTO profile (id, first_name, last_name, full_name, city, state, languages, school, company_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        for index, row in df.iterrows():
            for i in range(len(row)):
                if pd.isna(row[i]):
                    row[i] = None
                
            data_to_insert = tuple(row)
            try:
                cursor.execute(query, data_to_insert)
                cnx.commit()
                print(f"Linha {index + 1} inserida com sucesso.")
            except mysql.connector.Error as err:
                print(f"Erro ao inserir linha {index + 1}: {err}")
                cnx.rollback()  

        cursor.execute("SELECT COUNT(*) FROM profile")
        result = cursor.fetchone()
        print(f"Total de registros na tabela profile: {result[0]}")

    except mysql.connector.Error as err:
        print(f"Erro de conexão MySQL: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()