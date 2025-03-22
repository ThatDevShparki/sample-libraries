from sfz.sfz import SfzHeader


def main():
    regions = [
        SfzHeader(
            key='region',
            opcodes={
                'sample': './samples/rode_nt1_b2_med.wav',
                'key': 'b2',
                'lovel': 43,
                'hivel': 85,
                'amp_veltrack': 0,
            },
        )
        for _ in range(25)
    ]
    groups = [
        SfzHeader(
            key='group',
            opcodes={
                'ampeg_attack': '0.04',
                'ampeg_release': '0.45',
            },
            subheaders=regions,
        )
        for _ in range(5)
    ]

    master = SfzHeader(key='global', subheaders=groups)

    print(master)


if __name__ == '__main__':
    main()
