from pathlib import Path
from pydantic import BaseModel, field_validator


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


class Portfolio(BaseModel):
    name: str
    job_title: str
    image_url: str | None | Path
    about: str
    contact: Contact
    links: list[Link]
    skills: list[Skill]
    projects: list[Project]
    cv: list[Company]

    @field_validator("image_url")
    def convert_image(cls, v):
        if isinstance(v, str):
            return Path(v)
