from __future__ import annotations

import io
from collections.abc import Iterable
from typing import Any, TypeVar

T = TypeVar('T')

""" base types """


class SfzHeader:
    key: str
    subheaders: list[SfzHeader]
    opcodes: dict[str, Any]

    def __init__(
        self,
        key: str,
        subheaders: list[SfzHeader] | None = None,
        opcodes: dict[str, Any] | None = None,
    ):
        self.key = key
        self.opcodes = opcodes or {}
        self.subheaders = subheaders or []

    def __str__(self) -> str:
        buffer = io.StringIO()
        buffer.writelines(line + '\n' for line in self.serialize())
        return buffer.getvalue()

    def serialize(self) -> Iterable[str]:
        if self.subheaders or len(self.opcodes) > 5:
            yield f'<{self.key}>'

            for op_name, op_val in self.opcodes.items():
                yield f'{op_name}={op_val}'

            if self.subheaders:
                yield ''
            for child in self.subheaders:
                yield from child.serialize()

            yield ''
        else:
            yield f'<{self.key}> ' + ' '.join(
                f'{op_name}={op_val}' for op_name, op_val in self.opcodes.items()
            )
