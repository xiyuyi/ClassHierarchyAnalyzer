from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

from inheritscan.agents.microchains.chains.mock import MockChain
from inheritscan.agents.microchains.prompts.class_summary import (
    class_summary_prompt_english, class_summary_prompt_english_1_paragraph)
from inheritscan.agents.microchains.shared.llm_config import (
    get_qwen_coder_instruct500, get_qwen_coder_instruct2000)


def get_methods2class_chain(chain_name):
    if chain_name == "mock_chain":
        # Return the mock chain wrapped in RunnableMap
        mock_chain = MockChain()
        return RunnableMap({"class_summary": mock_chain})
    else:
        if chain_name == "qwen_coder_32b_instruct500_engilsh":
            llm = get_qwen_coder_instruct500()
            prompt = class_summary_prompt_english

        elif chain_name == "qwen_32b_1_paragraph":
            llm = get_qwen_coder_instruct500()
            prompt = class_summary_prompt_english_1_paragraph

        elif chain_name == "qwen_coder_32b_instruct2000_engilsh":
            llm = get_qwen_coder_instruct2000()
            prompt = class_summary_prompt_english

        chain = prompt | llm | StrOutputParser()
        return RunnableMap({"class_summary": chain})
