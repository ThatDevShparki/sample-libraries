from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Generic, TypeVar

T = TypeVar('T')

""" base types """


class SfzBase(Generic[T]):
    key: str

    def __init_subclass__(cls, key: str) -> None:
        cls.key = key

    def __init__(self, value: T) -> None:
        self.value = value

    def serialize(self) -> Iterable[str]:
        raise NotImplementedError

    def __str__(self) -> str:
        return '\n'.join(self.serialize())


class SfzOpcode(SfzBase[str], key='opcode'):
    def serialize(self) -> Iterable[str]:
        yield f'{self.key}={self.value}'


S = TypeVar('S', bound='SfzOpcode | SfzBlock[Any]')


class SfzBlock(SfzBase[Iterable[S]], key='opcode'):
    def serialize(self) -> Iterable[str]:
        opcodes = [value for value in self.value if isinstance(value, SfzOpcode)]
        blocks = [value for value in self.value if isinstance(value, SfzBlock)]

        if blocks or len(opcodes) > 5:
            yield f'<{self.key}>'

            for opcode in opcodes:
                yield from opcode.serialize()

            if blocks:
                yield ''
            for block in blocks:
                yield from block.serialize()

            yield ''
        else:
            yield f'<{self.key}> ' + ' '.join(
                line for opcode in opcodes for line in opcode.serialize()
            )


""" opcodes"""


class SfzOpSample(SfzOpcode, key='sample'):
    pass


class SfzOpKey(SfzOpcode, key='key'):
    pass


class SfzOpLovel(SfzOpcode, key='lovel'):
    pass


class SfzOpHivel(SfzOpcode, key='hivel'):
    pass


class SfzOpAmpVeltrack(SfzOpcode, key='amp_veltrack'):
    pass


class SfzOpAmpegAttack(SfzOpcode, key='ampeg_attack'):
    pass


class SfzOpAmpegRelease(SfzOpcode, key='ampeg_release'):
    pass


""" headers """


class SfzHeaderRegion(
    SfzBlock[SfzOpSample | SfzOpKey | SfzOpLovel | SfzOpHivel | SfzOpAmpVeltrack],
    key='region',
):
    pass


class SfzHeaderGroup(
    SfzBlock[SfzHeaderRegion | SfzOpAmpegAttack | SfzOpAmpegRelease], key='group'
):
    pass


class SfzHeaderMaster(SfzBlock[SfzHeaderGroup], key='master'):
    pass
