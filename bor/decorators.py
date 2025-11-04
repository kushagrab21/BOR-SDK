"""
Module: decorators
------------------
Provides @step decorator for marking deterministic reasoning steps.

Design goals:
- Enforce a clean step signature: (state, C, V)
- Allow optional display name via @step(name="...").
- Attach metadata so BoRRun can display a stable step name.
- No external dependencies.
"""

from typing import Callable, Optional
import inspect
from bor.exceptions import DeterminismError

_STEP_NAME_ATTR = "__bor_step_name__"
_IS_STEP_ATTR = "__bor_is_step__"

def _validate_signature(fn: Callable) -> None:
    """
    Ensure the function has a compatible signature:
      def fn(state, C, V): ...
    We accept positional-only/normal args; no *args/**kwargs for v0.1.
    """
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    if len(params) != 3:
        raise DeterminismError(
            f"BoR step `{fn.__name__}` must accept exactly 3 params: (state, C, V)."
        )

    # Disallow VAR_POSITIONAL (*args) and VAR_KEYWORD (**kwargs) for v0.1
    for p in params:
        if p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            raise DeterminismError(
                f"BoR step `{fn.__name__}` must not use *args/**kwargs in v0.1."
            )

def step(fn: Optional[Callable] = None, *, name: Optional[str] = None):
    """
    Usage:
        @step
        def normalize(s, C, V): ...

        @step(name="map_accounts")
        def map_fn(s, C, V): ...

    Returns the original function, tagged with BoR metadata.
    """
    def _decorate(f: Callable) -> Callable:
        _validate_signature(f)
        setattr(f, _IS_STEP_ATTR, True)
        setattr(f, _STEP_NAME_ATTR, name or f.__name__)
        return f

    # Support both @step and @step(name="...")
    if fn is not None and callable(fn):
        return _decorate(fn)
    return _decorate

