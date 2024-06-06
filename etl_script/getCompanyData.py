import requests
import json
# import mysql.connector
from classes.company import Company
from classes.company import Hq
from classes.company import Location
from classes.company import SimilarCompany
from dataclasses import asdict

output_file_path = 'results/linkedin_company.json'
company_result_data = []

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


def getCompany(companyData, cursor):
    print("Obtendo dados da empresa...")

    company_result_data = []  

    for data in companyData:
        if isinstance(data, dict):
            company = Company(
                linkedin_internal_id=data.get('linkedin_internal_id', 'N/A'),
                description=data.get('description', 'N/A'),
                website=data.get('website', 'N/A'),
                industry=data.get('industry', 'N/A'),
                company_size=data.get('company_size', [0]),
                company_size_on_linkedin=data.get('company_size_on_linkedin', 0),
                hq=Hq(
                    country=data.get('hq', {}).get('country', 'N/A'),
                    city=data.get('hq', {}).get('city', 'N/A'),
                    postal_code=data.get('hq', {}).get('postal_code', 'N/A'),
                    line_1=data.get('hq', {}).get('line_1', 'N/A'),
                    is_hq=data.get('hq', {}).get('is_hq', False),
                    state=data.get('hq', {}).get('state', 'N/A')
                ),
                company_type=data.get('company_type', 'N/A'),
                founded_year=data.get('founded_year', 0),
                specialties=data.get('specialities', []),
                locations=[Location(
                    country=loc.get('country', 'N/A'),
                    city=loc.get('city', 'N/A'),
                    postal_code=loc.get('postal_code', 'N/A'),
                    line_1=loc.get('line_1', 'N/A'),
                    is_hq=loc.get('is_hq', False),
                    state=loc.get('state', 'N/A')
                ) for loc in data.get('locations', [])],
                name=data.get('name', 'N/A'),
                tagline=data.get('tagline', 'N/A'),
                universal_name_id=data.get('universal_name_id', 'N/A'),
                profile_pic_url=data.get('profile_pic_url', 'N/A'),
                background_cover_image_url=data.get('background_cover_image_url', 'N/A'),
                search_id=data.get('search_id', 'N/A'),
                similar_companies=[SimilarCompany(
                    name=comp.get('name', 'N/A'),
                    link=comp.get('link', 'N/A'),
                    industry=comp.get('industry', 'N/A'),
                    location=comp.get('location', 'N/A')
                ) for comp in data.get('similar_companies', [])],
                updates=data.get('updates', []),
                follower_count=data.get('follower_count', 0)
            )

            company_result_data.append(asdict(company))

            company_size_str = ', '.join(map(str, company.company_size))
            specialties_str = ', '.join(map(str, company.specialties))

            company_data_tuple = (
                company.linkedin_internal_id, company.description, company.website, company.industry, 
                company_size_str, company.company_size_on_linkedin, company.hq.country, 
                company.hq.city, company.hq.postal_code, company.hq.line_1, company.hq.is_hq, 
                company.hq.state, company.company_type, company.founded_year, specialties_str, 
                company.name, company.tagline, company.universal_name_id, company.profile_pic_url, 
                company.background_cover_image_url, company.search_id, company.follower_count
            )

            add_company = (
                "INSERT INTO company (linkedin_internal_id, description, website, industry, company_size, company_size_on_linkedin, hq_country, hq_city, hq_postal_code, hq_line_1, hq_is_hq, hq_state, company_type, founded_year, specialties, name, tagline, universal_name_id, profile_pic_url, background_cover_image_url, search_id, follower_count) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(add_company, company_data_tuple)



        else:
            print("O item não é um dicionário válido:", data)

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(company_result_data, outfile, indent=4, ensure_ascii=False)

    print("Dados da empresa obtidos com sucesso!")




    # linkedin_internal_id: str = "N/A"
    # description: str = "N/A"
    # website: str = "N/A"
    # industry: str = "N/A"
    # company_size: List[int] = field(default_factory=lambda: [0])
    # company_size_on_linkedin: int = 0
    # hq: Hq = field(default_factory=Hq)
    # company_type: str = "N/A"
    # founded_year: int = 0
    # specialties: List[str] = field(default_factory=list)
    # locations: List[Location] = field(default_factory=list)
    # name: str = "N/A"
    # tagline: str = "N/A"
    # universal_name_id: str = "N/A"
    # profile_pic_url: str = "N/A"
    # background_cover_image_url: str = "N/A"
    # search_id: str = "N/A"
    # similar_companies: List[SimilarCompany] = field(default_factory=list)
    # updates: List[object] = field(default_factory=list)
    # follower_count: int = 0


        # add_company = (
        #     "INSERT INTO company ( company_id, company_name, employee_count, employee_range, hq_city, hq_country, hq_region, industries, linkedin_url, specialties, company_type, website) "
        #     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # )
    #     company_data_tuple = (company_id, company_name, employee_count, employee_range, hq_city, hq_country, hq_region, industries, linkedin_url, specialties, company_type, website)
    #     # cursor.execute(add_company, company_data_tuple)
    