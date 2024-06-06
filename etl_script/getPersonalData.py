import requests
import json
import os
# import mysql.connector
from classes.personal import Profile
profile_result_data = []

# def get_linkedin_profile(linkedin_url, headers):
#     base_url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-linkedin-profile"
#     params = {
#         'linkedin_url': linkedin_url,
#         'include_skills': 'false',
#         'include_certifications': 'false',
#         'include_publications': 'false',
#         'include_honors': 'false',
#         'include_volunteers': 'false',
#         'include_projects': 'false',
#         'include_patents': 'false',
#         'include_courses': 'false',
#         'include_organizations': 'false'
#     }
#     response = requests.get(base_url, headers=headers, params=params)

#     if response.status_code != 200:
#         print(f"Erro ao obter o perfil do LinkedIn: {response.status_code}")
#         return {}

#     return response.json()

def generateTable(cursor):
    print("Criando tabela de Personal...")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS personal (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        full_name VARCHAR(255),
        headline VARCHAR(255),
        about TEXT,
        city VARCHAR(255),
        country VARCHAR(255),
        state VARCHAR(255),
        linkedin_url TEXT,
        languages VARCHAR(255),
        job_title VARCHAR(255),
        school VARCHAR(255),
        company VARCHAR(255)
    );
    """

    cursor.execute(create_table_query)

    print("Tabela criada.")



def getPersonal(profileData, cursor):
    print("Obtendo dados pessoais...")

    generateTable(cursor)

    profile_result_data = []  # Lista para armazenar os dados dos perfis
    
    for data in profileData:
        if isinstance(data, dict):
            # Processing languages
            languages_list = data.get('languages', [])
            languages = ', '.join(languages_list) if languages_list else 'N/A'
            
            # Processing job title (current job)
            experiences = data.get('experiences', [])
            if experiences:
                job_title = experiences[0].get('title', 'N/A')
                company = experiences[0].get('company', 'N/A')
            else:
                job_title = 'N/A'
                company = 'N/A'
            
            # Processing education
            education = data.get('education', [])
            if education:
                school = education[0].get('school', 'N/A')
            else:
                school = 'N/A'
            
            personal = Profile(
                first_name=data.get('first_name', 'N/A'),
                last_name=data.get('last_name', 'N/A'),
                full_name=data.get('full_name', 'N/A'),
                headline=data.get('headline', 'N/A'),
                about=data.get('summary', 'N/A'),
                city=data.get('city', 'N/A'),
                country=data.get('country_full_name', 'N/A'),
                state=data.get('state', 'N/A'),
                linkedin_url=data.get('public_identifier', 'N/A'),
                languages=languages,
                job_title=job_title,
                company=company,
                school=school
            )
            
            profile_result_data.append(personal.__dict__)

            add_profile = """
                INSERT INTO personal (
                    first_name, last_name, full_name, headline, about, city, country, state, linkedin_url, languages, job_title, school, company
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            profile_data_tuple = (
                personal.first_name, personal.last_name, personal.full_name, personal.headline, personal.about, personal.city, personal.country, personal.state, personal.linkedin_url, personal.languages, personal.job_title, personal.school, personal.company)
            cursor.execute(add_profile, profile_data_tuple)


        else:
            print("O item não é um dicionário válido:", data)



    current_dir = os.path.dirname(__file__)
    output_file_path = os.path.join(current_dir, 'results', 'linkedin_personal.json')
    # Abrindo o arquivo fora do loop for
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(profile_result_data, outfile, indent=4, ensure_ascii=False)
        
    print("Dados pessoais obtidos com sucesso!")

    
    
    