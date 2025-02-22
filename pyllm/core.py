import logging

import pydantic

from pyllm.llm_adapter import LLM


def llm(*args, **kwargs):
    input_param_names = kwargs.keys()
    instructions = args
    if isinstance(instructions, str):
        instructions = [instructions]

    logging.info(
        f"to implement a llm function using {input_param_names} and {instructions}"
    )

    def lambda_function(*args, **kwargs):
        return None

    return lambda_function
