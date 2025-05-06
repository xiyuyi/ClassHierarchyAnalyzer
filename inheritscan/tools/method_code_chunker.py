from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import ast
import textwrap


def chunk_method_code(source: str) -> list[str]:

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        log.debug(f"❌ Syntax error in input code: {e}")
        return []

    chunks = []
    class_or_func = tree.body[0]
    if isinstance(class_or_func, ast.ClassDef):
        class_body = class_or_func.body
        method = next(
            (
                n
                for n in class_body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ),
            None,
        )
    elif isinstance(class_or_func, (ast.FunctionDef, ast.AsyncFunctionDef)):
        method = class_or_func
    else:
        print(
            "❌ Input must be a single function or class with at leaset one method."
        )
        return []

    if method is None:
        log.info("❌ No method found in the class.")
        return []

    method_src_lines = source.splitlines()
    indent = len(method_src_lines[0]) - len(method_src_lines[0].lstrip())
    base_indent = " " * indent

    # Chunk header
    header_line = method_src_lines[method.lineno - 1]
    chunks.append(header_line)

    buffer = []

    def flush_buffer():
        if buffer:
            chunks.append(base_indent + "\n".join(buffer))
            buffer.clear()

    control_types = (
        ast.If,
        ast.For,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncWith,
        ast.AsyncFor,
        ast.Match,  # Python 3.10+
    )

    for stmt in method.body:
        stmt_code = ast.get_source_segment(source, stmt)
        if not stmt_code:
            continue
        stmt_code = textwrap.dedent(stmt_code.strip())

        if isinstance(stmt, control_types):
            flush_buffer()
            chunks.append(textwrap.indent(stmt_code, base_indent))
        else:
            buffer.append(stmt_code)

    flush_buffer()
    return chunks
