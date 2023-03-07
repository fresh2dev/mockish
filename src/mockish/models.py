from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, TypeVar

from . import constants

T = TypeVar("T", bound="Response")


@dataclass
class ResponseData:
    status_code: int
    headers: dict[str, str]
    content: bytes | None
    elapsed: timedelta | None


class Response(ABC):
    @abstractmethod
    def __init__(
        self,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
        content: str | None = None,
        content_type: str | None = None,
        encoding: str | None = None,
        elapsed: timedelta | None = None,
        _data: ResponseData | None = None,
    ) -> None:
        ...

    @staticmethod
    def _prepare_response_data(
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
        content: str | None = None,
        content_type: str | None = None,
        encoding: str | None = None,
        elapsed: timedelta | None = None,
    ) -> ResponseData:
        if not headers:
            headers = {}

        if content:
            if not content_type:
                content_type = constants.CONTENT_TYPE_DEFAULT

            content_encoded: bytes

            if encoding:
                content_encoded = content.encode(encoding)
                content_type += f"; charset={encoding}"
            else:
                content_encoded = content.encode()

            headers["Content-Type"] = content_type

            if "Content-Length" not in headers:
                headers["Content-Length"] = str(len(content_encoded))

        return ResponseData(
            status_code=int(status_code) if status_code else 200,
            headers=headers,
            content=content_encoded,
            elapsed=elapsed,
        )

    @classmethod
    def create(cls: type[T], data: ResponseData) -> T:
        return cls(_data=data)

    @classmethod
    def from_dict(cls: type[T], content: dict[str, Any], **kwargs: Any) -> T:
        return cls.create(
            cls._prepare_response_data(
                content=json.dumps(content, ensure_ascii=False),
                content_type="application/json",
                **kwargs,
            ),
        )

    @classmethod
    def from_file(cls: type[T], path: str, encoding: str = "utf-8", **kwargs: Any) -> T:
        with open(path, encoding=encoding) as f:
            return cls.create(
                cls._prepare_response_data(
                    content=f.read(),
                    content_type=(
                        "application/json" if path.lower().endswith(".json") else None
                    ),
                    **kwargs,
                ),
            )
