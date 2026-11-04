"""JSON input/output that keeps monetary values exact.

Numbers with a decimal point are read as ``Decimal`` and written back as plain
JSON numbers, so a case file the founder typed by hand keeps its values when
the tool rewrites the sections it owns.
"""

from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path
from typing import Any

_MARK = "@@BVDEC@@"
_MARK_RE = re.compile('"' + re.escape(_MARK) + r"([-+0-9.eE]+)" + re.escape(_MARK) + '"')


def loads(text: str) -> Any:
    return json.loads(text, parse_float=Decimal)


def load(path: Path) -> Any:
    return loads(Path(path).read_text(encoding="utf-8"))


def _default(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        if not obj.is_finite():
            raise ValueError(f"non-finite number cannot be stored: {obj}")
        # Always write a decimal point: a whole-number Decimal written as "600" would be read back as
        # the int 600, losing its Decimal type (json only maps numbers with a point to parse_float).
        text = format(obj, "f")
        if "." not in text:
            text += ".0"
        return f"{_MARK}{text}{_MARK}"
    raise TypeError(f"not JSON serialisable: {type(obj).__name__}")


def dumps(obj: Any) -> str:
    text = json.dumps(obj, indent=2, ensure_ascii=False, default=_default)
    return _MARK_RE.sub(lambda m: m.group(1), text) + "\n"


def dump(obj: Any, path: Path) -> None:
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(dumps(obj), encoding="utf-8")
    tmp.replace(path)


def canonical(obj: Any) -> str:
    """Stable serialisation used only for fingerprints."""

    def default(o: Any) -> Any:
        if isinstance(o, Decimal):
            return {"$dec": str(o)}
        raise TypeError(f"not JSON serialisable: {type(o).__name__}")

    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=default)


def fingerprint(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()
