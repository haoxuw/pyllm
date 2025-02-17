import logging

import pydantic

from pyllm.llm import LLM


class Functor:
    def __init__(self):
        pass

    @classmethod
    def __call__(cls, **kwargs):
        input_param_names = kwargs.keys()

        annotations = cls.pseudocode.__annotations__
        params = {
            input_param: annotations[input_param] for input_param in input_param_names
        }
        return_value = annotations["return"]

        schemas = {}
        for schema_def in list(params.values()) + [return_value]:
            # pylint: disable=unidiomatic-typecheck
            if type(schema_def) == type(pydantic.BaseModel):
                schemas[schema_def.__name__] = schema_def.model_json_schema()

        logging.info(
            f"todo: implement this class with schema defined by inputs: {params}, and return {return_value}\nWhere schemas are: {schemas}"
        )

        context, instructions = cls.pseudocode(**kwargs)

        llm_response = LLM.text_completion(
            system=context,
            user=instructions,
            max_tokens=10000,
        )

        # todo: parse llm_response into the schema defined by return_value
        return_value = llm_response

        return return_value

    @staticmethod
    def pseudocode(**kwargs):
        pass
