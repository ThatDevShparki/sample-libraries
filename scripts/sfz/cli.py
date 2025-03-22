import os
import re
from pathlib import Path

import click

from sfz.midi import note_name_to_number
from sfz.sfz import SfzHeader

SAMPLE_PATTERN = re.compile(
    r'^(?P<micBrand>\w*?)_(?P<micSerial>\w*?)_(?P<note>\w*?(?:_chord)?)_(?P<range>\w*?).wav$'
)


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def generate(path: str) -> None:
    _path = Path(path)

    # find all possible instruments
    click.echo('Searching for instrument samples...')
    samples_paths: dict[str, Path] = {}
    for instrument_path in _path.iterdir():
        if not instrument_path.is_dir():
            continue
        if 'samples' in os.listdir(instrument_path):
            _instrument_name = instrument_path.name
            _samples_path = instrument_path.joinpath('samples')
            click.echo(f' -> Found samples for {_instrument_name} at {_samples_path}')
            samples_paths[_instrument_name] = _samples_path
        else:
            click.echo(f'    (No samples folder found in {instrument_path})')
    click.echo(f'Found {len(samples_paths)} instruments.')
    click.echo()

    click.echo('Generating SFZ files...')
    for instrument_name, samples_path in samples_paths.items():
        # categorize samples
        click.echo(f' -> Generating SFZ for {instrument_name}...')
        low_samples: list[tuple[str, str]] = []
        med_samples: list[tuple[str, str]] = []
        high_samples: list[tuple[str, str]] = []

        for _, _, files in samples_path.walk():
            for file in files:
                match = re.match(SAMPLE_PATTERN, file)
                if not match:
                    print(f"found a file that doesn't match the pattern {file}")
                    continue

                _, _, key_name, vel_range = match.groups()

                key_name = key_name.replace('s', '#').lower().strip()
                if '_chord' in key_name:
                    key_name = key_name.replace('_chord', '') + '1'
                else:
                    octave = int(key_name[-1])
                    key_name = key_name[:-1] + str(octave + 1)
                key_idx = str(note_name_to_number(key_name))

                vel_range = vel_range.lower().strip()
                if vel_range == 'low':
                    low_samples.append((file, key_idx))
                elif vel_range == 'med':
                    med_samples.append((file, key_idx))
                else:
                    high_samples.append((file, key_idx))

        # create sfz_groups
        sfz_low_group = SfzHeader(
            'group',
            opcodes={
                'lovel': 1,
                'hivel': 42,
            },
            subheaders=[
                SfzHeader(
                    'region',
                    opcodes={
                        'sample': file,
                        'key': key,
                    },
                )
                for (file, key) in low_samples
            ],
        )
        sfz_med_group = SfzHeader(
            'group',
            opcodes={
                'lovel': 43,
                'hivel': 85,
            },
            subheaders=[
                SfzHeader(
                    'region',
                    opcodes={
                        'sample': file,
                        'key': key,
                    },
                )
                for (file, key) in med_samples
            ],
        )
        sfz_high_group = SfzHeader(
            'group',
            opcodes={
                'lovel': 86,
                'hivel': 127,
            },
            subheaders=[
                SfzHeader(
                    'region',
                    opcodes={
                        'sample': file,
                        'key': key,
                    },
                )
                for (file, key) in high_samples
            ],
        )

        sfz_global = SfzHeader(
            'global',
            subheaders=[sfz_low_group, sfz_med_group, sfz_high_group],
            opcodes={
                'ampeg_attack': 0.04,
                'ampeg_release': 0.45,
                'amp_veltrack': 0,
                'loop_mode': 'loop_sustain',
                'loop_start': 10000,
                'loop_end': 30000,
            },
        )

        sfz_control = SfzHeader(
            'control',
            opcodes={'default_path': 'samples/'},
            subheaders=[sfz_global],
        )

        # write file
        successes = 0
        instrument_sfz_path = samples_path.parent.joinpath(f'{instrument_name}.sfz')
        click.echo(f'    writing to {instrument_sfz_path}')
        try:
            with open(instrument_sfz_path, 'w') as f:
                f.write(str(sfz_control))
            click.echo(f'    Successfully generated SFZ file for {instrument_name}')
            successes += 1
        except Exception as e:
            click.echo(f'    error writing to {instrument_sfz_path}: {e}')
        click.echo(
            f'Successfully generated SFZ files for {successes}/{len(samples_paths)} instruments.'
        )


@cli.command()
def lint() -> None:
    click.echo('Linting....')


if __name__ == '__main__':
    cli()
