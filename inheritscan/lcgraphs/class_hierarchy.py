from langgraph.graph import StateGraph

from inheritscan.agents.codescanner_agent import CodeScannerAgent
from inheritscan.agents.mcinheritance_agent import MCInheritance
from inheritscan.agents.network_builder_agent import NetworkBuilderAgent


class ClassHierarchyGraphBuilder:
    def __init__(self):
        self.scanner = CodeScannerAgent()
        self.inheritance_analyzer = MCInheritance()
        self.network_builder = NetworkBuilderAgent()
        self.graph = None
        self.compiled_graph = None

    def compile_graph(self):
        self.graph = StateGraph(dict)
        self.graph.add_node("scanner", self.scanner)
        self.graph.add_node("inheritance_analyzer", self.inheritance_analyzer)
        self.graph.add_node("network_builder", self.network_builder)

        self.graph.add_edge("scanner", "inheritance_analyzer")
        self.graph.add_edge("inheritance_analyzer", "network_builder")

        self.graph.set_entry_point("scanner")
        self.graph.set_finish_point("network_builder")

        self.compiled_graph = self.graph.compile()
        return self.compiled_graph
