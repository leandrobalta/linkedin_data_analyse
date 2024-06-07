from dataclasses import dataclass
from datetime import datetime

@dataclass
class JobClass:
    position: str
    company: str
    companyLogo: str
    location: str
    date: datetime
    agoTime: str
    salary: str
    jobUrl: str