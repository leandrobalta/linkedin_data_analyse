import json
from getPersonalData import getPersonal
from getCompanyData import getCompany
from getJobData import getJob
import mysql.connector 
import os

# headers = {
#     'x-rapidapi-key': "a1bfe33833msh346eb3fa3de3e52p1a2a9cjsn61a1ea7eab70",
#     'x-rapidapi-host': "fresh-linkedin-profile-data.p.rapidapi.com"

# }


if __name__ == "__main__":
    # Conectando ao banco de dados
    cnx = mysql.connector.connect(user="unifei", password="unifei", host="25.59.203.106", database="linkedin_data", port = 3306)
    cursor = cnx.cursor()

    if cnx.is_connected():
        print("Conexão ao MySQL realizada com sucesso.")
        
        cursor.execute("select full_name, company_id from profile limit 1;")
        for row in cursor.fetchall():
            print(row)

                


    else:
        print("Erro ao conectar ao MySQL.")

    current_dir = os.path.dirname(__file__)

    while True:
        handleOption = input("\n1: Profiles\n2: Company\n3: Job\n4: Save and Exit\n5: Exit\nChoose an option: ")

        if handleOption == "1":
            file_path = os.path.join(current_dir, "results/new_linkedin_personal.json")
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            getPersonal(data, cursor)

        elif handleOption == "2":
            file_path = os.path.join(current_dir, "jsonData/newCompanyData.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
            getCompany(data, cursor)
            

        elif handleOption == "3":
            file_path = os.path.join(current_dir, "jsonData/newJobData.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
            getJob(data, cursor)

          
        elif handleOption == "4":
            cnx.commit()
            cursor.close()
            cnx.close()
            print("Data saved and connection closed. Exiting program.")
            break

        elif handleOption == "5":
            print("Exiting without saving.")
            break

        else:
            print("Invalid option. Please choose a valid option.")
