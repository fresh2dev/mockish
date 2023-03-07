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
        """A `requests.Response` object, useful when mocking/patching HTTP calls.

        Args:
            status_code:
            headers:
            content:
            content_type:
            encoding:
            elapsed:

        Examples:
            *Common imports*
            >>> from mockish import Mock, patch
            >>> from mockish.requests import Response
            >>> import requests

            - `mockish.requests.Response`
            >>> resp: requests.Response = Response(content='hello world')
            >>> resp.content
            b'hello world'
            >>> resp.status_code
            200

            - `mockish.requests.Response.from_dict(...)`
            >>> resp: requests.Response = Response.from_dict(
            ...     {'hello': 'world'},
            ...     status_code=201
            ... )
            >>> resp.json()
            {'hello': 'world'}
            >>> resp.status_code
            201
            >>> resp.headers
            {'Content-Type': 'application/json', 'Content-Length': '18'}

            - Mocking a `requests` session:
            >>> session = Mock(spec_set=requests.Session, **{
            ...     'get': Mock(
            ...         return_once=Response.from_dict({'hello': 'world'})
            ...     ),
            ...     'post': Mock(
            ...         return_once=Response.from_dict(
            ...             {'hello': 'world'},
            ...             status_code=201
            ...         ),
            ...     ),
            ... })
            >>> session.get('https://www.fresh2.dev')
            <Response [200]>
            >>> session.post('https://www.fresh2.dev')
            <Response [201]>

            - Complete example with patching:
            >>> mock_resp = Response.from_dict({'hello': 'world'})
            >>> with patch.object(
            ...     requests,
            ...     'get',
            ...     Mock(return_once=mock_resp)
            ... ):
            ...     resp: requests.Response = requests.get('https://www.fresh2.dev')
            ...     requests.get.assert_called_once()
            >>> resp
            <Response [200]>
            >>> resp.json()
            {'hello': 'world'}
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
