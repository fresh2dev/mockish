from typing import Any, Callable, Dict, Optional, Sequence
from unittest import mock

from pydantic import validate_arguments

__all__ = [
    "Mock",
    "AsyncMock",
    "patch_fastapi_dependencies",
]


class _AsyncMock(mock.Mock):
    # AsyncMock for Python 3.7
    # (added to stdlib in Python 3.8)

    # pylint: disable=invalid-overridden-method, useless-parent-delegation
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return super().__call__(*args, **kwargs)


@validate_arguments(config={"arbitrary_types_allowed": True})
def _build_mock(
    *,
    is_async: bool,
    return_value: Optional[Any] = None,
    return_call: Optional[Callable[..., Optional[Any]]] = None,
    return_once: Optional[Any] = None,
    return_each: Optional[Sequence[Any]] = None,
    return_exception: Optional[Exception] = None,
    side_effect: Optional[Any] = None,
    **kwargs: Any,
) -> mock.Mock:
    if (
        sum(
            [
                bool(return_value),
                bool(return_once),
                bool(return_each),
                bool(return_call),
                bool(return_exception),
                bool(side_effect),
            ],
        )
        > 1
    ):
        raise ValueError("Specify exactly one argument.")

    if side_effect:
        kwargs["side_effect"] = side_effect

    elif return_value:
        kwargs["side_effect"] = lambda *args, **kwargs: return_value

    elif return_call:
        kwargs["side_effect"] = return_call

    elif return_once:
        kwargs["side_effect"] = [return_once]

    elif return_each:
        kwargs["side_effect"] = return_each

    elif return_exception:
        kwargs["side_effect"] = return_exception

    return _AsyncMock(**kwargs) if is_async else mock.Mock(**kwargs)


def Mock(
    *,
    return_value: Optional[Any] = None,
    return_call: Optional[Callable[..., Optional[Any]]] = None,
    return_once: Optional[Any] = None,
    return_each: Optional[Sequence[Any]] = None,
    return_exception: Optional[Exception] = None,
    **kwargs: Any,
) -> mock.Mock:
    """A thin wrapper around [unittest.mock.Mock](https://docs.python.org/3/library/unittest.mock.html#the-mock-class) to abstract away the use of `side_effect` in favor of these explicit `return_X` parameters:

    Args:
        return_value: return the given value
        return_call: return the value returned by the given callable
        return_once: return the given value exactly once
        return_each: consecutively return each element of the given iterable
        return_exception: raise the given exception

    Returns:
        : A `Mock` object

    Examples:
        - `return_value`
        >>> obj = Mock(return_value='hello world')
        >>> obj()
        'hello world'

        - `return_call`
        >>> func = lambda: 'hello world'
        >>> obj = Mock(return_call=func)
        >>> obj()
        'hello world'

        - `return_once`
        >>> obj = Mock(return_once='hello world')
        >>> obj()
        'hello world'
        >>> obj()
        Traceback (most recent call last):
        ...
        StopIteration

        - `return_each`
        >>> obj = Mock(return_each=[1, 2, 3])
        >>> obj()
        1
        >>> obj()
        2
        >>> obj()
        3
        >>> obj()
        Traceback (most recent call last):
        ...
        StopIteration

        - `return_exception`:
        >>> obj = Mock(return_exception=ValueError("hello world"))
        >>> obj()
        Traceback (most recent call last):
        ...
        ValueError: hello world
    """
    return _build_mock(
        is_async=False,
        return_value=return_value,
        return_call=return_call,
        return_once=return_once,
        return_each=return_each,
        return_exception=return_exception,
        **kwargs,
    )


def AsyncMock(
    *,
    return_value: Optional[Any] = None,
    return_call: Optional[Callable[..., Optional[Any]]] = None,
    return_once: Optional[Any] = None,
    return_each: Optional[Sequence[Any]] = None,
    return_exception: Optional[Exception] = None,
    **kwargs: Any,
) -> mock.Mock:
    """Same as `mockish.Mock`, but returns an async `Mock`.

    Returns:
        : An async `Mock` object
    """
    return _build_mock(
        is_async=True,
        return_value=return_value,
        return_call=return_call,
        return_once=return_once,
        return_each=return_each,
        return_exception=return_exception,
        **kwargs,
    )


def patch_fastapi_dependencies(
    *args: Any,
    overrides: Optional[Dict[Callable[..., Any], Callable[..., Any]]],
    remove: bool = False,
) -> None:
    """Recursively patch dependencies of FastAPI instance(s).

    [Read about FastAPI test dependencies.](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
    > Note: `fastapi` must be installed.

    Args:
        *args: One or more FastAPI instances
        overrides: A mapping of overrides, or `None` to clear all
        remove: Remove the provided overrides

    Raises:
        TypeError: raised if any of `args` is not a FastAPI instance

    Returns:
        : No value returned

    Examples:
        ```py
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        app = FastAPI(...)

        mockish.patch_fastapi_dependencies(
            app,
            overrides={
                get_app_settings: lambda: app_settings,
            },
        )

        @app.get("/")
        def get() -> dict[str, str]:
            return {"hello": "world"}

        return TestClient(app)
        ```
    """
    from fastapi import FastAPI  # pylint: disable=import-error
    from starlette.routing import Mount  # pylint: disable=import-error

    for x in args:
        if not isinstance(x, FastAPI):
            raise TypeError(f"Expected type 'FastAPI'; given: {type(x)}")

        if overrides is None:
            x.dependency_overrides.clear()
        elif remove:
            for k in overrides:
                del x.dependency_overrides[k]
        else:
            x.dependency_overrides.update(overrides)

        patch_fastapi_dependencies(
            *[
                y.app
                for y in x.routes
                if isinstance(y, Mount) and isinstance(y.app, FastAPI)
            ],
            overrides=overrides,
            remove=remove,
        )
