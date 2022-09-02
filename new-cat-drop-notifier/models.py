"""
Custom models and types
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from bs4 import Tag

from consts import OHS_BASE_URL

AnimalType = Literal["dogs", "cats", "small", "horsefarm"]


@dataclass(frozen=True)
class AnimalAdoptionCard:
    """Represents 1 adoption card item from the /adopt page"""
    id: int | None
    added_timestamp: datetime
    animal_type: AnimalType | str
    details_endpoint: str
    name: str | None
    breed: str | None
    sex: str | None
    color: str | None
    age: str | None

    def __str__(self) -> str:
        out = f"""\n
Name: {self.name}
Age: {self.age}
Breed: {self.breed}
Sex: {self.sex}
Color: {self.color}
Details: {OHS_BASE_URL}{self.details_endpoint}
        """
        return out

    @classmethod
    def from_raw_result_item(cls, result_item: Tag):
        """Will initialize card from a raw HTML result-item"""
        obj = cls(
            id=int(str(next(iter(result_item.find_next("span", {"class": "id"}).contents), None))),
            added_timestamp=datetime.fromtimestamp(float(result_item["data-ohssb-ts"])),
            animal_type=result_item["data-ohssb-type"],
            details_endpoint=str(result_item.find_next("a")["href"]),
            name=str(next(iter(result_item.find_next("span", {"class": "name"}).contents), None)),
            breed=str(next(iter(result_item.find_next("span", {"class": "breed"}).contents), None)),
            sex=str(next(iter(result_item.find_next("span", {"class": "sex"}).contents), None)),
            color=str(next(iter(result_item.find_next("span", {"class": "color"}).contents), None)),
            age=str(next(iter(result_item.find_next("span", {"class": "age"}).contents), None))
        )
        return obj
