from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Hq:
    country: str = "N/A"
    city: str = "N/A"
    postal_code: str = "N/A"
    line_1: str = "N/A"
    is_hq: bool = False
    state: str = "N/A"

@dataclass
class Location:
    country: str = "N/A"
    city: str = "N/A"
    postal_code: str = "N/A"
    line_1: str = "N/A"
    is_hq: bool = False
    state: str = "N/A"

@dataclass
class SimilarCompany:
    name: str = "N/A"
    link: str = "N/A"
    industry: str = "N/A"
    location: Optional[str] = "N/A"

@dataclass
class Company:
    linkedin_internal_id: str = "N/A"
    description: str = "N/A"
    website: str = "N/A"
    industry: str = "N/A"
    company_size: List[int] = field(default_factory=lambda: [0])
    company_size_on_linkedin: int = 0
    hq: Hq = field(default_factory=Hq)
    company_type: str = "N/A"
    founded_year: int = 0
    specialties: List[str] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    name: str = "N/A"
    tagline: str = "N/A"
    universal_name_id: str = "N/A"
    profile_pic_url: str = "N/A"
    background_cover_image_url: str = "N/A"
    search_id: str = "N/A"
    similar_companies: List[SimilarCompany] = field(default_factory=list)
    updates: List[object] = field(default_factory=list)
    follower_count: int = 0
