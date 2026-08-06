from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    city: str
    postal_code: str | int
    country: str


class Contact(BaseModel):
    email: str
    location: Location


class Link(BaseModel):
    name: str
    url: str


class Skill(BaseModel):
    name: str
    attributes: list[str]


class Project(BaseModel):
    name: str
    attributes: list[str]
    link: Link


class Station(BaseModel):
    role: str
    start_year: int
    end_year: int | None
    activities: str


class Company(BaseModel):
    name: str
    stations: list[Station]


class CV(BaseModel):
    jobs: list[Company] = Field(default_factory=list)
    education: list[Company] = Field(default_factory=list)


class Portfolio(BaseModel):
    name: str
    job_title: str
    image_url: str | None | Path
    about: str
    contact: Contact
    links: list[Link]
    skills: list[Skill]
    projects: list[Project]
    cv: CV

    @field_validator("cv", mode="before")
    def normalize_cv(cls, v):
        if isinstance(v, list):
            return {"jobs": v, "education": []}
        return v

    @field_validator("image_url")
    def convert_image(cls, v):
        if isinstance(v, str):
            return Path(v)
