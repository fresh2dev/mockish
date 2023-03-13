# mockish

> A thin layer of sugar atop Python's mock.

| Links         |                                                   |
|---------------|---------------------------------------------------|
| Code Repo     | https://www.github.com/fresh2dev/mockish          |
| Mirror Repo   | https://www.Fresh2.dev/code/r/mockish             |
| Documentation | https://www.Fresh2.dev/code/r/mockish/i           |
| Changelog     | https://www.Fresh2.dev/code/r/mockish/i/changelog |
| License       | https://www.Fresh2.dev/code/r/mockish/i/license   |
| Funding       | https://www.Fresh2.dev/funding                    |

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/fresh2dev/mockish?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/mockish/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/fresh2dev/mockish?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/mockish/releases)
[![License](https://img.shields.io/github/license/fresh2dev/mockish?color=blue&style=for-the-badge)](https://www.Fresh2.dev/code/r/mockish/i/license)
[![GitHub issues](https://img.shields.io/github/issues-raw/fresh2dev/mockish?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/mockish/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/fresh2dev/mockish?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/mockish/pulls)
[![GitHub Repo stars](https://img.shields.io/github/stars/fresh2dev/mockish?color=blue&style=for-the-badge)](https://star-history.com/#fresh2dev/mockish&Date)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mockish?color=blue&style=for-the-badge)](https://pypi.org/project/mockish)
[![Docs Website](https://img.shields.io/website?down_message=unavailable&label=docs&style=for-the-badge&up_color=blue&up_message=available&url=https://www.Fresh2.dev/code/r/mockish/i)](https://www.Fresh2.dev/code/r/mockish/i)
[![Coverage Website](https://img.shields.io/website?down_message=unavailable&label=coverage&style=for-the-badge&up_color=blue&up_message=available&url=https://www.Fresh2.dev/code/r/mockish/i/tests/coverage)](https://www.Fresh2.dev/code/r/mockish/i/tests/coverage)
[![Funding](https://img.shields.io/badge/funding-%24%24%24-blue?style=for-the-badge)](https://www.Fresh2.dev/funding)

*Brought to you by...*

[![](https://img.fresh2.dev/fresh2dev.svg)](https://www.fresh2.dev)

---

## Overview

`mockish` is a small tool I built to make life easier when writing tests in Python.

It provides:

1. Explicit alternatives to the nuanced `mock.Mock(side_effect=...)` argument, including:

    - `mockish.Mock(return_value=...)`
    - `mockish.Mock(return_call=...)`
    - `mockish.Mock(return_once=...)`
    - `mockish.Mock(return_each=...)`
    - `mockish.Mock(return_exception=...)`

2. Methods for creating HTTP responses -- both `requests.Response` and `httpx.Response` objects -- that can be returned by the Mock, including:

    - `mockish.httpx.Response.from_dict(...)`
    - `mockish.requests.Response.from_dict(...)`

## Install

From [PyPi](https://pypi.org/project/mockish/){:target="_blank"}:

```py
pip install mockish
```

## Use

Complete example of mocking a HTTP response:

```py
from mockish import Mock, patch
from mockish.requests import Response
import requests

mock_resp = Response.from_dict({'hello': 'world'})

with patch.object(
    requests,
    'get',
    Mock(return_once=mock_resp)
):
    resp: requests.Response = requests.get('https://www.fresh2.dev')

    requests.get.assert_called_once()

print(resp)
> <Response [200]>

print(resp.json())
> {'hello': 'world'}
```

See the reference docs for more examples:

- [mockish.Mock](https://www.Fresh2.dev/code/r/mockish/i/reference/01)
- [mockish.httpx.Response](https://www.Fresh2.dev/code/r/mockish/i/reference/02)
- [mockish.requests.Response](https://www.Fresh2.dev/code/r/mockish/i/reference/03)

## Support

If this project delivers value to you, please [provide feedback](https://github.com/fresh2dev/mockish/issues), code contributions, and/or [funding](https://www.Fresh2.dev/funding).
