import requests
import json
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

def getJob(jobData, cursor):
    print("Obtendo Jobs...")
    job_result_data = []

    for job_data in jobData:
        # Convertendo o campo 'date' para datetime
        date_str = job_data.get("date", "N/A")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = None
        
        auxJob = JobClass(
            position=job_data.get("position", "N/A"),
            company=job_data.get("company", "N/A"),
            companyLogo=job_data.get("companyLogo", "N/A"),
            location=job_data.get("location", "N/A"),
            date=date,
            agoTime=job_data.get("agoTime", "N/A"),
            salary=job_data.get("salary", "N/A"),
            jobUrl=job_data.get("jobUrl", "N/A")
        )
        # Convert datetime to string for JSON serialization
        job_dict = asdict(auxJob)
        job_dict["date"] = auxJob.date.strftime("%Y-%m-%d") if auxJob.date else "N/A"
        job_result_data.append(job_dict)

        add_job = ("INSERT INTO job (position, company, companyLogo, location, date, agoTime, salary, jobUrl) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        
        job_data_tuple = (job_dict["position"], job_dict["company"], job_dict["companyLogo"], job_dict["location"], job_dict["date"], job_dict["agoTime"], job_dict["salary"], job_dict["jobUrl"])
        cursor.execute(add_job, job_data_tuple)



    with open(output_file_path, 'w') as outfile:
        json.dump(job_result_data, outfile, indent=4)


    print(f"Dados inseridos.")



