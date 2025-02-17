import enum

import pydantic

import pyllm


class Object(pydantic.BaseModel):
    description: str


class Character(pydantic.BaseModel):
    name: str


class Duelist(Object, Character):
    pass


class Origin(str, enum.Enum):
    COMICS = "comics"
    TV = "tv"
    REAL_LIFE = "real_life"
    OTHER = "other"


class DuelistInfo(pydantic.BaseModel):
    short_description: str
    is_sentient: bool
    origin: Origin
    abilities: list[str]
    weaknesses: list[str]


class DuelResult(pydantic.BaseModel):
    would_win: bool
    reason: str
    short_story_what_happend: str
    long_story_what_happend: str


class Explain(pyllm.Functor):
    def pseudocode(duelist: Duelist) -> DuelistInfo:
        context = "In canonical universe, at prime age and health, with all powers, abilities and equipments."
        instructions = [
            f"Explain the powers of the DUELIST",
        ]
        return context, instructions


class Duel(pyllm.Functor):
    def pseudocode(challenger: DuelistInfo, opponent: DuelistInfo) -> bool:
        context = "Who would win? Be reasonable, logical and funny. Use imagination and common sense."
        instructions = [
            f"Suppose the CHALLENGER and the OPPONENT duel, which one would win",
            "short story should be under 50 words, long story should be under 200 words",
            "reason should analize the abilities and weaknesses",
            "if CHALLENGER would win, set would_win to True, otherwise False",
        ]
        return context, instructions


clark = Character(name="Superman")
kryptonite = Object(description="kryptonite")
bruce = Character(name="Batman")

explain = Explain()
duel = Duel()

duel = duel(challenger=explain(duelist=clark), opponent=explain(duelist=kryptonite))
print(duel)
