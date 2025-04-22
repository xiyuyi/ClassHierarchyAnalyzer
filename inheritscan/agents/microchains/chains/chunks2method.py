from langchain_core.runnables import RunnableMap
from inheritscan.agents.microchains.chains.mock import MockChain


def get_chunks2method_chain(chain_name):
    if chain_name == "mock_chain":
            # Return the mock chain wrapped in RunnableMap
            mock_chain = MockChain()
            return RunnableMap({"method_summary": mock_chain})
