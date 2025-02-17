from pyllm.database import cached_staticmethod
from pyllm.llm_providers import open_ai


class LLM:
    def __init__(self, provider_name: str):
        if provider_name == "openai":
            self.provider = open_ai
        elif provider_name == "azure":
            raise NotImplementedError("Azure provider is not implemented yet")
        elif provider_name == "anthropic":
            raise NotImplementedError("Anthropic provider is not implemented yet")
        else:
            raise ValueError("Invalid provider name")

    @cached_staticmethod
    @staticmethod
    def text_completion(system: str, user: str, max_tokens: int = 10000):
        # return self.provider.text_completion()
        # raise NotImplementedError("This method is not implemented yet")
        return "hello world!"
