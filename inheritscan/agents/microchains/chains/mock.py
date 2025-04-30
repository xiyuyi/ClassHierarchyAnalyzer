from typing import Any, Dict, Optional

from langchain.schema.runnable import Runnable


class MockChain(Runnable):
    """A mock chain that returns a fixed response."""

    def invoke(
        self, input: Any, config: Optional[Any] = None
    ) -> Dict[str, str]:
        return "this is mock chain"

    async def ainvoke(
        self, input: Any, config: Optional[Any] = None
    ) -> Dict[str, str]:
        return "this is mock chain"
