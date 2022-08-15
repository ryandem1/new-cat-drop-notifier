"""
Custom models and types
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from bs4 import Tag


AnimalType = Literal["dogs", "cats", "small", "horsefarm"]


@dataclass(frozen=True)
class AnimalAdoptionCard:
    """Represents 1 adoption card item from the /adopt page"""
    id: int
    added_timestamp: datetime
    animal_type: AnimalType | str
    details_endpoint: str
    name: str
    breed: str
    sex: str
    color: str
    age: str

    @classmethod
    def from_raw_result_item(cls, result_item: Tag):
        """Will initialize card from a raw HTML result-item"""
        obj = cls(
            id=int(str(result_item.find_next("span", {"class": "id"}).contents[0])),
            added_timestamp=datetime.fromtimestamp(float(result_item["data-ohssb-ts"])),
            animal_type=result_item["data-ohssb-type"],
            details_endpoint=str(result_item.find_next("a")["href"]),
            name=str(result_item.find_next("span", {"class": "name"}).contents[0]),
            breed=str(result_item.find_next("span", {"class": "breed"}).contents[0]),
            sex=str(result_item.find_next("span", {"class": "sex"}).contents[0]),
            color=str(result_item.find_next("span", {"class": "color"}).contents[0]),
            age=str(result_item.find_next("span", {"class": "age"}).contents[0])
        )
        return obj
