# pyllm

pyllm minimizes the effort needed to use LLMs within classical python software.

It aims to abstract away the complexities related to schema declaration, parsing and validation.

Next steps, we will also add support for multiple LLM service providers, performance benchmarking, and caching.

## Usage

```python
from pydantic import BaseModel

class AnimalFacts(BaseModel):
    habitat: str
    life_span: int
    is_endangered: bool
    facts: list[str]

def explain(animal: str) -> AnimalFacts:
    instructions = [
        "Explain facts about the animal",
        "About the most common breed",
        "Each fact in less than 30 words"
    ]
    return instructions

facts = explain(animal="monkey")
```