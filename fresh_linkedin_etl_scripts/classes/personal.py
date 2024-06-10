from dataclasses import dataclass

@dataclass
class Profile:
    first_name: str = 'N/A'
    last_name: str = 'N/A'
    full_name: str = 'N/A'
    about: str = 'N/A'
    city: str = 'N/A'
    country: str = 'N/A'
    state: str = 'N/A'
    linkedin_url: str = 'N/A'
    languages: str = 'N/A'
    school: str = 'N/A'
    company_id: int = 'N/A'