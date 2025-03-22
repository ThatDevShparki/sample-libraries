import re

NOTE_NAMES_SEQ_FROM_C = [
    ['c'],
    ['c#', 'db'],
    ['d'],
    ['d#', 'eb'],
    ['e'],
    ['f'],
    ['f#', 'gb'],
    ['g'],
    ['g#', 'ab'],
    ['a'],
    ['a#', 'bb'],
    ['b'],
]
NOTE_INDEX_C1 = 24
NOTE_NAME_PATTERN = re.compile(r'(?P<name>[aAbBcCdDeEfFgG][#b]?)(?P<octave>\d)')


def note_name_to_number(name: str) -> int | None:
    match = re.match(NOTE_NAME_PATTERN, name.lower().strip())
    if not (match and all(match.groups())):
        return
    note_name, note_octave = map(str, match.groups())

    note_number = 0
    for idx, values in enumerate(NOTE_NAMES_SEQ_FROM_C):
        if note_name not in values:
            continue
        note_number = (int(note_octave) - 1) * 12 + idx + NOTE_INDEX_C1
    return note_number
