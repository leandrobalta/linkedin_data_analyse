import requests
import json
import os
from datetime import datetime
from classes.jobClass import JobClass
from dataclasses import asdict

output_file_path = 'results/linkedin_job.json'
job_result_data = []

# def get_linkedin_job(headers):
#     base_url = "https://fresh-linkedin-profile-data.p.rapidapi.com/search-jobs?geo_code=103644278&date_posted=any_time&function_id=it%2Csale&industry_code=4%2C5&sort_by=most_relevant&start=0&easy_apply=false&under_10_applicants=false"
#     params = {
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
#         print(f"Erro ao obter Jobs do LinkedIn: {response.status_code}")
#         return {}

#     return response.json()

def generateTable(cursor):
    print("Criando tabela de Job...")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS job (
        id INT AUTO_INCREMENT PRIMARY KEY,
        position VARCHAR(255),
        company VARCHAR(255),
        company_logo VARCHAR(255),
        location VARCHAR(255),
        date DATE,
        ago_time VARCHAR(255),
        salary VARCHAR(255),
        job_url TEXT
    );
    """

    cursor.execute(create_table_query)

    print("Tabela criada.")

def getJob(jobData, cursor):
    print("Obtendo Jobs...")

    generateTable(cursor)
    
    job_result_data = []


    for job_data in jobData:
        # Convertendo o campo 'date' para datetime
        date_str = job_data.get("date", "N/A")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = None
        
        job = JobClass(
            position=job_data.get("position", "N/A"),
            company=job_data.get("company", "N/A"),
            companyLogo=job_data.get("companyLogo", "N/A"),
            location=job_data.get("location", "N/A"),
            date=date.strftime("%Y-%m-%d") if date else "N/A",
            agoTime=job_data.get("agoTime", "N/A"),
            salary=job_data.get("salary", "N/A"),
            jobUrl=job_data.get("jobUrl", "N/A")
        )
        # Convert datetime to string for JSON serialization
        job_dict = asdict(job)
        job_result_data.append(job_dict)

        add_job = ("INSERT INTO job (position, company, company_logo, location, date, ago_time, salary, job_url) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        
        job_data_tuple = (job.position, job.company, job.companyLogo, job.location, job.date, job.agoTime, job.salary, job.jobUrl)
        cursor.execute(add_job, job_data_tuple)



    current_dir = os.path.dirname(__file__)
    output_file_path = os.path.join(current_dir, 'results', 'linkedin_job.json')
    
    with open(output_file_path, 'w') as outfile:
        json.dump(job_result_data, outfile, indent=4)


    print(f"Dados inseridos.")



