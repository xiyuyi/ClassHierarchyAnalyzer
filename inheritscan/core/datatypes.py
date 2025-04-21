from abc import ABC
from dataclasses import dataclass, field, asdict
from typing import Optional, List
from datetime import datetime, timezone


@dataclass
class CodeInfo(ABC):
    id: Optional[str] = ""
    code: Optional[str] = ""
    summary: Optional[str] = ""
    module_path: Optional[str] = ""
    class_name: Optional[str] = ""
    created_time: Optional[str] = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        return CodeInfo(
            id=data["id"],
            code=data["code"],
            summary=data.get("summary"),
            module_path = data.get("module_path"),
            class_name = data.get("class_name"),
            created_time=data.get("created_time", datetime.now(timezone.utc).isoformat()),
        )


@dataclass
class SnippetInfo(CodeInfo):
    method_name: Optional[str] = ""


@dataclass
class MethodInfo(CodeInfo):
    snippets: List[SnippetInfo] = field(default_factory=list)
    def add_snippet_info(self, snippet_info: SnippetInfo):
        self.snippets.append(snippet_info)


@dataclass
class ClassInfo(CodeInfo):
    methods: List[MethodInfo] = field(default_factory=list)
    def add_method_info(self, method_info: MethodInfo):
        self.snippets.append(method_info)
