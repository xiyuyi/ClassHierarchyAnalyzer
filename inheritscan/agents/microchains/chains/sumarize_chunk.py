from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

from inheritscan.agents.microchains.chains.mock import MockChain
from inheritscan.agents.microchains.prompts.chunk_summary import (
    chunk_summary_prompt_english, chunk_summary_prompt_korean)
from inheritscan.agents.microchains.shared.llm_config import (
    get_qwen_coder_instruct500, get_tinyllm150)


def get_chunk_summary_chain(chain_name):
    """
    implemented the following typs of chain_names:
    """
    print(f"chain name is: {chain_name}")
    if chain_name == "mock_chain":
        # Return the mock chain wrapped in RunnableMap
        mock_chain = MockChain()
        return RunnableMap({"chunk_summary": mock_chain})

    else:
        if chain_name == "tinyllama150_korean":
            llm = get_tinyllm150()
            prompt = chunk_summary_prompt_korean

        elif chain_name == "qwen_coder_32b_instruct500_engilsh":
            llm = get_qwen_coder_instruct500()
            prompt = chunk_summary_prompt_english

        chain = prompt | llm | StrOutputParser()
        return RunnableMap({"chunk_summary": chain})
