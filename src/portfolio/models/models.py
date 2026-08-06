from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    street: str | None = None
    house_number: str | None = None
    city: str
    postal_code: str | int | None = None
    country: str | None = None


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
    education: list[Company] = Field(default_factory=list)
    jobs: list[Company] = Field(default_factory=list)

    @field_validator("image_url")
    def convert_image(cls, v):
        if isinstance(v, str):
            return Path(v)
        return v
