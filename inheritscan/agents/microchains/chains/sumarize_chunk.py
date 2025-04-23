from typing import Any, Dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain.schema.runnable import Runnable
from typing import Any, Dict, Optional

from inheritscan.agents.microchains.chains.mock import MockChain
from inheritscan.agents.microchains.shared.llm_config import get_tinyllm150
from inheritscan.agents.microchains.prompts.chunk_summary import (
    chunk_summary_prompt_korean,
)


def get_chunk_summary_chain(chain_name):
    if chain_name == "tinyllama150_korean":
        llm = get_tinyllm150()
        # Wrap in a single output parser to maintain JSON formatting
        chunk_summary_chain = chunk_summary_prompt_korean | llm | StrOutputParser()

        # Wrap in RunnableMap so it's consistent with other chains
        return RunnableMap({"chunk_summary": chunk_summary_chain})

    elif chain_name == "mock_chain":
        # Return the mock chain wrapped in RunnableMap
        mock_chain = MockChain()
        return RunnableMap({"chunk_summary": mock_chain})
