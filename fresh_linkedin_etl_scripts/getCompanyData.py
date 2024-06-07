import requests
import json
import os
# import mysql.connector
from classes.company import Company

# def get_linkedin_company(linkedin_url, headers):
#     base_url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-company-by-linkedinurl"
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
#         print(f"Erro ao obter a empresa do LinkedIn: {response.status_code}")
#         return {}

#     return response.json()

def generateTable(cursor):
    print("Criando tabela de Company...")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS company (
        id INT AUTO_INCREMENT PRIMARY KEY,
        linkedin_internal_id VARCHAR(255) UNIQUE,
        description TEXT,
        website VARCHAR(255),
        industry VARCHAR(255),
        company_size VARCHAR(255),
        company_size_on_linkedin INT,
        company_type VARCHAR(255),
        founded_year INT,
        specialties TEXT,
        country VARCHAR(255),
        state VARCHAR(255),
        city VARCHAR(255),
        name VARCHAR(255),
        tagline VARCHAR(255),
        universal_name_id VARCHAR(255),
        search_id VARCHAR(255),
        follower_count INT
    );
    """

    cursor.execute(create_table_query)

    print("Tabela criada.")


def getCompany(companyData, cursor):
    print("Obtendo dados da empresa...")
    
    generateTable(cursor)

    company_result_data = []  

    for data in companyData:
        if isinstance(data, dict):
            # Processar listas e strings corretamente
            company_size = data.get('company_size', [0])
            if not isinstance(company_size, list):
                company_size = [company_size]

            specialties = data.get('specialities', [])
            if not isinstance(specialties, list):
                specialties = [specialties]

            locations = data.get('locations', [])
            if not isinstance(locations, list):
                locations = [locations]

            for loc in locations:
                country = loc.get('country', 'N/A')
                state = loc.get('state', 'N/A')
                city = loc.get('city', 'N/A')

            company = Company(
                linkedin_internal_id=data.get('linkedin_internal_id', 'N/A'),
                description=data.get('description', 'N/A'),
                website=data.get('website', 'N/A'),
                industry=data.get('industry', 'N/A'),
                company_size=company_size,
                company_size_on_linkedin=data.get('company_size_on_linkedin', 0),
                company_type=data.get('company_type', 'N/A'),
                founded_year=data.get('founded_year', 0),
                specialties=specialties,
                country=country,
                state=state,
                city=city,
                name=data.get('name', 'N/A'),
                tagline=data.get('tagline', 'N/A'),
                universal_name_id=data.get('universal_name_id', 'N/A'),
                search_id=data.get('search_id', 'N/A'),
                follower_count=data.get('follower_count', 0)
            )

            company_result_data.append(company.__dict__)

            company_size_str = ', '.join(map(str, company.company_size))
            specialties_str = ', '.join(map(str, company.specialties))


            company_data_tuple = (
                company.linkedin_internal_id, company.description, company.website, company.industry, 
                company_size_str, company.company_size_on_linkedin, company.company_type, company.founded_year, specialties_str, 
                company.country, company.state, company.city,company.name, company.tagline, company.universal_name_id, company.search_id, 
                company.follower_count
            )

            add_company = (
                "INSERT INTO company (linkedin_internal_id, description, website, industry, company_size, company_size_on_linkedin, company_type, founded_year, specialties, country, state, city, name, tagline, universal_name_id, search_id, follower_count)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(add_company, company_data_tuple)



        else:
            print("O item não é um dicionário válido:", data)


    current_dir = os.path.dirname(__file__)
    output_file_path = os.path.join(current_dir, 'results', 'linkedin_company.json')
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(company_result_data, outfile, indent=4, ensure_ascii=False)

    print("Dados da empresa obtidos com sucesso!")