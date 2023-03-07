from __future__ import annotations

import json
from random import randint
from typing import Any
from uuid import uuid4

import httpx
import pytest

import mockish
from mockish.constants import CONTENT_TYPE_DEFAULT, CONTENT_TYPE_JSON


@pytest.mark.parametrize(
    ("content", "content_type"),
    [
        ("asdf", None),
        ("asdf", "asdf"),
        (json.dumps({"hello": "asdf"}), None),
        (json.dumps({"hello": "asdf"}), CONTENT_TYPE_JSON),
    ],
)
def test_mock_response(content: str, content_type: str | None) -> None:
    expected_content: str = content
    expected_content_type: str | None = content_type
    expected_status_code: int = 200 + randint(0, 99)
    expected_headers: dict[str, str] = {"User-Agent": str(uuid4())}

    mock_resp: httpx.Response = mockish.httpx.Response(
        content=expected_content,
        content_type=expected_content_type,
        status_code=expected_status_code,
        headers=expected_headers,
    )

    assert isinstance(mock_resp, httpx.Response)

    assert "Content-Type" in mock_resp.headers
    assert "Content-Length" in mock_resp.headers

    assert mock_resp.text == expected_content
    assert mock_resp.content == expected_content.encode()
    assert int(mock_resp.headers["Content-Length"]) == len(mock_resp.content)

    if not expected_content_type:
        expected_content_type = CONTENT_TYPE_DEFAULT
    elif expected_content_type == CONTENT_TYPE_JSON:
        assert mock_resp.json() == json.loads(expected_content)

    assert mock_resp.headers["Content-Type"] == expected_content_type

    assert mock_resp.encoding == "utf-8"

    assert expected_headers
    for k, v in expected_headers.items():
        assert mock_resp.headers[k] == v
        assert mock_resp.headers[k.lower()] == v
        assert mock_resp.headers[k.upper()] == v


def test_mock_response_from_dict() -> None:
    mock_resp: httpx.Response = mockish.httpx.Response.from_dict(
        {"hello": str(uuid4())},
    )

    assert isinstance(mock_resp, httpx.Response)

    assert "Content-Length" in mock_resp.headers
    assert "Content-Type" in mock_resp.headers

    test_mock_response(
        content=mock_resp.text,
        content_type=mock_resp.headers["Content-Type"],
    )


def _assert_mock_response_values(
    mock_session,
    responses: list[httpx.Response],
) -> None:
    for expected in responses:
        fake_endpoint: str = str(uuid4())
        observed: httpx.Response = mock_session.get(fake_endpoint)

        mock_session.get.assert_called_with(fake_endpoint)

        assert isinstance(observed, httpx.Response)
        assert observed == expected

    assert mock_session.get.call_count == len(responses)


def test_mock_request_method_return_value() -> None:
    n_calls: int = 5

    mock_resp: httpx.Response = mockish.httpx.Response.from_dict(
        content={"hello": str(uuid4())},
        status_code=200 + randint(0, 99),
    )

    with mockish.patch.object(httpx, "get", mockish.Mock(return_value=mock_resp)):
        _assert_mock_response_values(
            mock_session=httpx,
            responses=[mock_resp] * n_calls,
        )

        try:
            httpx.get(...)
        except StopIteration:
            pytest.fail("this method should return the value indefinitely")


def test_mock_request_method_return_values() -> None:
    n_responses: int = 5

    mock_resp_list: list[httpx.Response] = [
        mockish.httpx.Response.from_dict(
            content={"hello": str(uuid4())},
            status_code=200 + randint(0, 99),
        )
        for _ in range(n_responses)
    ]

    with mockish.patch.object(httpx, "get", mockish.Mock(return_each=mock_resp_list)):
        _assert_mock_response_values(mock_session=httpx, responses=mock_resp_list)

        with pytest.raises(StopIteration):
            httpx.get(...)


def test_mock_request_method_callable() -> None:
    n_calls = 5

    mock_resp: httpx.Response = mockish.httpx.Response.from_dict(
        {"hello": str(uuid4())},
    )

    def my_func(
        *args: Any,  # pylint: disable=unused-argument
        **kwargs: Any,  # pylint: disable=unused-argument
    ) -> httpx.Response:
        return mock_resp

    with mockish.patch.object(httpx, "get", mockish.Mock(return_call=my_func)):
        _assert_mock_response_values(
            mock_session=httpx,
            responses=[mock_resp] * n_calls,
        )

        try:
            httpx.get(...)
        except StopIteration:
            pytest.fail("method should return the value indefinitely")
