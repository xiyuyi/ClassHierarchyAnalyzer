from langchain_core.runnables import RunnableMap
from inheritscan.agents.microchains.chains.mock import MockChain
from inheritscan.agents.microchains.shared.llm_config import get_qwen_coder_instruct500, get_tinyllm150
from langchain_core.output_parsers import StrOutputParser
from inheritscan.agents.microchains.prompts.class_summary import (
    class_summary_prompt_english
)


def get_methods2class_chain(chain_name):
    if chain_name == "mock_chain":
            # Return the mock chain wrapped in RunnableMap
            mock_chain = MockChain()
            return RunnableMap({"class_summary": mock_chain})
    else:
        if chain_name == "qwen_coder_32b_instruct500_engilsh":
            llm = get_qwen_coder_instruct500()
            prompt = class_summary_prompt_english

        chain = prompt | llm | StrOutputParser()
        return RunnableMap({"class_summary": chain})

     # TODO #6: design a minichain for this class.
    # future may need to try different models.
    # think about how to aggregate the method summaries ( consider aggregate from the .json files)
    # considerations:
    #  summary missing, what to do.
    # the class file do not exist, what to do.
    # think about what needs to be checked to monitor performance.
    # don't worry about logging for now.
