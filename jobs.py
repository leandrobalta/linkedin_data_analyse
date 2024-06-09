import pandas as pd
import mysql.connector

def load_jobs():
    df_jobs= pd.read_csv("csvs/jobs.csv", encoding='utf-8')

    try:    
        cnx = mysql.connector.connect(
                user="unifei",
                password="unifei",
                host="localhost",
                database="explain_linkedin",
                port=3306,
            )
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT company_id FROM company")

        company_id_result = cursor.fetchall()
            
        company_id_array = []
        for company_id in company_id_result:
            company_id_array.append(company_id['company_id'])
            
        df_filtered = df_jobs[df_jobs['company_id'].isin(company_id_array)]
        df_final = df_filtered.loc[:, ['job_id', 'company_name', 'title', 'description', 'location', 'company_id', 'med_salary', 'remote_allowed', 'work_type', 'application_url', 'expiry']] #O .loc permite selecionar um subconjunto de linhas e colunas pelo rótulo.
        
        query = ("INSERT INTO job (job_id, company_name, title, description, location, company_id, med_salary, remote_allowed, work_type, application_url, expiry) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
      
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
        print(f"Total de registros na tabela jobs: {result}")

    except mysql.connector.Error as err:
        print(f"Erro de conexão MySQL: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
