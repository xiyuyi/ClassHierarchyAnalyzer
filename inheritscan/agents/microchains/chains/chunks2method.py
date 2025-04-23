from langchain_core.runnables import RunnableMap
from inheritscan.agents.microchains.chains.mock import MockChain


def get_chunks2method_chain(chain_name):
    if chain_name == "mock_chain":
            # Return the mock chain wrapped in RunnableMap
            mock_chain = MockChain()
            return RunnableMap({"method_summary": mock_chain})
    # TODO #5: design a tinyllama based chain for this class.
    # future may need to try different models.
    # think about how to aggregate the chunks summaries ( consider aggregate from the .json files)
    # considerations:
    # chunk summary missing, what to do.
    # the class file do not exist, what to do.
    # think about what needs to be checked to monitor performance.
    # don't worry about logging for now.
