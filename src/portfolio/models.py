from dataclasses import dataclass


@dataclass
class Location:
    city: str
    postal_code: str | int
    country: str


@dataclass
class Contact:
    email: str
    location: Location


@dataclass
class Link:
    name: str
    url: str


@dataclass
class Section:
    name: str
    attributes: list[str]
    link: Link


@dataclass
class Skill:
    name: str
    attributes: list[str]


@dataclass
class Project:
    name: str
    sections: list[Section]


@dataclass
class Station:
    role: str
    start_year: str
    end_year: str
    activities: str


@dataclass
class Company:
    name: str
    stations: list[Station]


@dataclass
class Portfolio:
    name: str
    job_title: str
    about: str
    contact: Contact
    links: list[Link]
    image_url: str | None
    skills: list[Skill]
    projects: list[Project]
    cv: list[Company]
