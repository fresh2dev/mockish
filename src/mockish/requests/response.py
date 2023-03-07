from __future__ import annotations

from datetime import timedelta

import requests

from .. import models


class Response(requests.Response, models.Response):
    def __init__(
        self,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
        content: str | None = None,
        content_type: str | None = None,
        encoding: str | None = None,
        elapsed: timedelta | None = None,
        _data: models.ResponseData | None = None,
    ):
        """

        Args:
            status_code:
            headers:
            content:
            content_type:
            encoding:
            elapsed:
            _data:

        """
        super().__init__()

        if not _data:
            _data = super()._prepare_response_data(
                status_code=status_code,
                headers=headers,
                content=content,
                content_type=content_type,
                encoding=encoding,
                elapsed=elapsed,
            )

        self.status_code = _data.status_code

        self.headers = requests.structures.CaseInsensitiveDict(_data.headers)

        if _data.content:
            self._content = _data.content

        if _data.elapsed:
            self.elapsed = _data.elapsed
