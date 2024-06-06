import json
from getPersonalData import getPersonal
from getCompanyData import getCompany
from getJobData import getJob
import mysql.connector 

# headers = {
#     'x-rapidapi-key': "a1bfe33833msh346eb3fa3de3e52p1a2a9cjsn61a1ea7eab70",
#     'x-rapidapi-host': "fresh-linkedin-profile-data.p.rapidapi.com"

# }


# Conectando ao banco de dados
cnx = mysql.connector.connect(user="unifei", password="unifei", host="25.59.203.106", database="linkedin", port = 3306)
cursor = cnx.cursor()


apiChoose = input("1: Profiles\n2: Company\n3: Job\nChoose an option: ")

if apiChoose == "1":
    with open("jsonData/newProfileData.json", 'r') as file:
        data = json.load(file)
        # print(data)
    getPersonal(data, cursor)

elif apiChoose == "2":
    with open("jsonData/newCompanyData.json", 'r') as file:
        data = json.load(file)
        # print(data)
    getCompany(data, cursor)

elif apiChoose == "3":
    with open("jsonData/newJobData.json", 'r') as file:
        data = json.load(file)
        # print(data)
    getJob(data, cursor)

else:
    print("Invalid option")
    exit()


cnx.commit()
cursor.close()
cnx.close()

