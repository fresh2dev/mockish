from __future__ import annotations

from datetime import timedelta

import httpx

from .. import models
from ..mockish import Mock


class Response(httpx.Response, models.Response):
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
        """A `httpx.Response` object, useful when mocking/patching HTTP calls.

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
            >>> from mockish.httpx import Response
            >>> import httpx

            - `mockish.httpx.Response`
            >>> resp: httpx.Response = Response(content='hello world')
            >>> resp.content
            b'hello world'
            >>> resp.status_code
            200

            - `mockish.httpx.Response.from_dict(...)`
            >>> resp: httpx.Response = Response.from_dict(
            ...     {'hello': 'world'},
            ...     status_code=201
            ... )
            >>> resp.json()
            {'hello': 'world'}
            >>> resp.status_code
            201
            >>> resp.headers
            Headers({'content-type': 'application/json', 'content-length': '18'})

            - Mocking a `httpx` session:
            >>> session = Mock(spec_set=httpx, **{
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
            <Response [200 OK]>
            >>> session.post('https://www.fresh2.dev')
            <Response [201 Created]>

            - Complete example with patching:
            >>> mock_resp = Response.from_dict({'hello': 'world'})
            >>> with patch.object(
            ...     httpx,
            ...     'get',
            ...     Mock(return_once=mock_resp)
            ... ):
            ...     resp: httpx.Response = httpx.get('https://www.fresh2.dev')
            ...     httpx.get.assert_called_once()
            >>> resp
            <Response [200 OK]>
            >>> resp.json()
            {'hello': 'world'}
        """

        super().__init__(status_code=200)

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

        self.headers = httpx.Headers(_data.headers)

        if _data.content:
            self._content = _data.content

        if _data.elapsed:
            self.elapsed = _data.elapsed

        self._request = Mock(spec_set=httpx.Request)
