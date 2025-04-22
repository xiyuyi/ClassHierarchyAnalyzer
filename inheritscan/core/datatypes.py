from abc import ABC
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
from datetime import datetime, timezone


def current_utc_time() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CodeInfo(ABC):
    id: Optional[str] = None
    code: Optional[str] = None
    summary: Optional[str] = None
    module_path: Optional[str] = None
    class_name: Optional[str] = None
    modified_time: Optional[str] = field(default_factory=current_utc_time)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def extract_shared_fields(cls, data: dict) -> dict:
        """Extract the fields shared by all subclasses."""
        return {
            "id": data.get("id"),
            "code": data.get("code"),
            "summary": data.get("summary"),
            "module_path": data.get("module_path"),
            "class_name": data.get("class_name"),
            "modified_time": data.get("modified_time", current_utc_time()),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**cls.extract_shared_fields(data))


@dataclass
class SnippetInfo(CodeInfo):
    """Represents a code snippet within a method."""

    method_name: Optional[str] = ""
    snippet_name: Optional[str] = ""
    chain_name: Optional[str] = ""

    @classmethod
    def from_dict(cls, data: dict):
        shared_fields = cls.extract_shared_fields(data)
        return cls(
            **shared_fields,
            method_name=data.get("method_name"),
            snippet_name=data.get("snippet_name"),
            chain_name=data.get("chain_name")
        )


@dataclass
class MethodInfo(CodeInfo):
    method_name: Optional[str] = ""
    snippets: Dict[str, SnippetInfo] = field(default_factory=dict)

    def add_snippet_info(self, snippet_info: SnippetInfo):
        self.snippets[snippet_info.snippet_name] = snippet_info

    @classmethod
    def from_dict(cls, data: dict):
        shared_fields = cls.extract_shared_fields(data)
        snippets = {
            name: SnippetInfo.from_dict(snippet_info)
            for name, snippet_info in data.get("snippets", {}).items()
        }
        return cls(
            **shared_fields, method_name=data.get("method_name"), snippets=snippets
        )


@dataclass
class ClassInfo(CodeInfo):
    methods: Dict[str, MethodInfo] = field(default_factory=dict)

    def add_method_info(self, method_info: MethodInfo):
        if not method_info.method_name:
            raise ValueError("method_info must have a valid 'method_name'.")
        self.methods[method_info.method_name] = method_info

    @classmethod
    def from_dict(cls, data: dict):
        shared_fields = cls.extract_shared_fields(data)
        methods = {
            name: MethodInfo.from_dict(method_data)
            for name, method_data in data.get("methods", {}).items()
        }
        return cls(**shared_fields, methods=methods)
