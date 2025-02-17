from dataclasses import dataclass

import pydantic


@dataclass
class Common:
    hashed_key: str = "hashed_key"
    key: str = "key"
    value: str = "value"
    cache_table: str = "cache_table"
    updated_at: str = "updated_at"
    created_at: str = "created_at"
    date_formats_python: tuple[str] = ("%Y/%m/%d", "%Y-%m-%d", "%Y%m%d")


class AnimalFacts(pydantic.BaseModel):
    habitat: str
    life_span: int
    is_endangered: bool
    facts: list[str]


def explain(animal: str) -> AnimalFacts:
    return [
        "Explain facts about the animal",
        "About the most common breed",
        "Less than 30 words each fact",
    ]


facts = explain(animal="monkey")
