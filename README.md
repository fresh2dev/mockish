# mockish

*A thin layer of sugar atop Python's mock.*

|             |                                    |
|-------------|------------------------------------|
| Code Repo   | https://github.com/fresh2dev/mockish  |
| Mirror Repo | https://www.Fresh2.dev/code/r/mockish |

![](https://img.fresh2.dev/fresh2dev.svg)

`mockish` is a small tool I built to make life easier when writing tests in Python. It provides:

1. Explicit alternatives to the nuanced `mock.Mock(side_effect=...)` argument, including:

- `mockish.Mock(return_value=...)`
- `mockish.Mock(return_call=...)`
- `mockish.Mock(return_once=...)`
- `mockish.Mock(return_each=...)`
- `mockish.Mock(return_exception=...)`

2. To help with mocking HTTP requests, `mockish` makes it easy to create `Response` objects to use as the return value for your Mock.

3. To serve as a drop in replacement for `mock`, the `mockish` module exports `mockish.patch`.

To be clear, `mockish` doesn't do much on its own, instead relying fully on the native `mock` library. This library just provides some syntactic sugar atop `mock` that acts in a way that I consider more intuitive.

If this project delivers value to you, please [provide feedback](https://github.com/fresh2dev/mockish/issues), code contributions, and/or [funding](https://www.Fresh2.dev/funding).

See my other projects @ https://www.Fresh2.dev/projects

## Install

## Use

See the reference docs for

### Mock Return Values

...

### Mock Objects

...

### Mock HTTP Responses

```py
mock_resp: httpx.Response = mockish.httpx.Response(
    content=expected_content,
    content_type=expected_content_type,
    status_code=expected_status_code,
    headers=expected_headers,
)

assert isinstance(mock_resp, httpx.Response)
```

```py
mock_resp: httpx.Response = mockish.httpx.Response.from_dict({"hello": str(uuid4())})

print(mock_resp.json())
```

### Complete Example

...
