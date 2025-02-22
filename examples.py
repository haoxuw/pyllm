import enum

from pydantic import BaseModel

from pyllm import llm

###############################################################
# a simple example
hello = llm("say hello in 10 different languages")


###############################################################
# # A Object-Oriented Programming (OOP) approach, with reliable input/output schema
class Anything(BaseModel):
    name: str
    description: str = None


class Origin(str, enum.Enum):
    COMICS = "comics"
    REAL_LIFE = "real_life"
    OTHER = "other"


class Attributes(BaseModel):
    short_description: str
    is_sentient: bool
    origin: Origin
    abilities: list[str]
    weaknesses: list[str]


batman = llm(
    "Explain powers",
    INPUT=Anything(name="Batman"),
    OUTPUT=Attributes,
)

# a more complex use case
kryptonite = Anything(name="kryptonite", description="A ton of those green rocks")
superman = llm(
    "Explain powers",
    INPUT=Anything(name="Superman"),
    OUTPUT=Attributes,
)


###############################################################
# # create a reusable function prototype
class Outcome(BaseModel):
    would_win: bool
    reason: str
    short_story_what_happend: str
    long_story_what_happend: str


battle = llm(
    [
        "Suppose the CHALLENGER and the OPPONENT duel, which one would win",
        "short story should be under 50 words, long story should be under 200 words",
        "reason should analize the abilities and weaknesses",
        "if CHALLENGER would win, set would_win to True, otherwise False",
    ],
    create_prototype=True,
    OUTPUT=Outcome,
)

match1 = battle(
    CHALLENGER=superman,
    OPPONENT=batman,
)


match2 = battle(
    CHALLENGER=kryptonite,
    OPPONENT=superman,
)
