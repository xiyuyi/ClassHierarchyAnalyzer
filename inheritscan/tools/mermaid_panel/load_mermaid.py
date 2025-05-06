from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)


def load_mermaid_scripts():
    # TODO
    output = """
    graph TD;
        A[Class A] --> B[Class B];
        A --> C[Class C];
        B --> D[Class D];
        C --> D;

        click A callNodeClick "Click A"
        click B callNodeClick "Click B"
        click C callNodeClick "Click C"
        click D callNodeClick "Click D"
    """
    return output
