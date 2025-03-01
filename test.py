from pyllm import Functor

client = OpenAI()


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def extract_event_information(description: str) -> CalendarEvent:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": description},
        ],
        response_format=CalendarEvent,
    )
    return completion


extract_event_information("Alice and Bob are going to a science fair on Friday.")


class EventExtractor(Functor):
    def __init__(self, model: str = "gpt-4o-2024-08-06"):
        super().__init__()

    # def pseudocode(description: str) -> CalendarEvent:
    #     context = ""
    #     task = [
    #         "Extract the event information"
    #     ]
    #     # format
    #     # example
    #     # persona
    #     # tone
    #     return context, instructions

    def context():
        return ""

    def task():
        return ["Extract the event information", "if missing, dont guess, leave empty"]

    def tone():
        return "formal"

    def preview_prompt():
        return ""


extractor = EventExtractor()
extractor(description="Alice and Bob are going to a science fair on Friday.")
