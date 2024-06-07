import pandas as pd
import mysql.connector

def main():
    file_path = "csvs/companies.csv"
    df_companies = pd.read_csv(file_path, encoding='utf-8')
    df_jobs= pd.read_csv("csvs/postings.csv", encoding='utf-8')
    df_companies_database = df_companies.head(1000)
    df_filtered = df_jobs[df_jobs['company_id'].isin(df_companies_database['company_id'])]
    # df_final = df_filtered[['job_id', 'company_name', 'title', 'description', 'location', 'company_id', 'med_salary', 'remote_allowed', 'work_type', 'application_url', 'expiry']]
    df_final = df_filtered.loc[:, ['job_id', 'company_name', 'title', 'description', 'location', 'company_id', 'med_salary', 'remote_allowed', 'work_type', 'application_url', 'expiry']]

    try:
        cnx = mysql.connector.connect(
            user="unifei",
            password="unifei",
            host="localhost",
            database="linkedin_data",
            port=3306,
        )
        cursor = cnx.cursor()

        # Preparando a query de inserção
        query = ("INSERT INTO job (job_id, company_name, title, description, location, company_id, med_salary, remote_allowed, work_type, application_url, expiry) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
      
        # Iterando sobre cada linha do DataFrame
        helper = 0
        for index, row in df_final.iterrows():
            for i in range(len(row)):
                if pd.isna(row[i]):
                    row[i] = None
                
            data_to_insert = tuple(row)
            try:
                cursor.execute(query, data_to_insert)
                cnx.commit()
                print(f"Linha {index + 1} inserida com sucesso.")
                helper += 1
                if helper == 4000:
                    break
            except mysql.connector.Error as err:
                print(f"Erro ao inserir linha {index + 1}: {err}")
                cnx.rollback()

        cursor.execute("SELECT COUNT(*) FROM job")
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
