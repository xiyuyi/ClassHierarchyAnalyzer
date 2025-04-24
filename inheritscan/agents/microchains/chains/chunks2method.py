from langchain_core.runnables import RunnableMap
from inheritscan.agents.microchains.chains.mock import MockChain
from langchain_core.output_parsers import StrOutputParser


from inheritscan.agents.microchains.shared.llm_config import get_qwen_coder_instruct500
from inheritscan.agents.microchains.prompts.method_summary import (
    method_summary_prompt_english
)

def get_chunks2method_chain(chain_name):
    if chain_name == "mock_chain":
            # Return the mock chain wrapped in RunnableMap
            mock_chain = MockChain()
            return RunnableMap({"method_summary": mock_chain})
    else:
        if chain_name == "qwen_coder_32b_instruct500_engilsh":
            llm = get_qwen_coder_instruct500()
            prompt = method_summary_prompt_english

        chain = prompt | llm | StrOutputParser()
        return RunnableMap({"method_summary": chain})
