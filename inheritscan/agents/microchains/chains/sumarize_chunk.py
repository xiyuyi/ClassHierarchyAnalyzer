from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

from inheritscan.agents.microchains.shared.llm_config import get_tinyllm150
from inheritscan.agents.microchains.prompts.chunk_summary import (
    chunk_summary_prompt_korean,
)


def get_chunk_summary_chain():
    llm = get_tinyllm150()

    # Wrap in a single output parser to maintain JSON formatting
    chunk_summary_chain = chunk_summary_prompt_korean | llm | StrOutputParser()

    # Wrap in RunnableMap so it's consistent with other chains
    composed_chain = RunnableMap({"chunk_summary": chunk_summary_chain})

    return composed_chain
