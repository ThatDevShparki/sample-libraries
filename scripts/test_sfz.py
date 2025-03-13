from sfz.types import (
    SfzHeaderGroup,
    SfzHeaderMaster,
    SfzHeaderRegion,
    SfzOpAmpegAttack,
    SfzOpAmpegRelease,
    SfzOpLovel,
    SfzOpSample,
)


def main():
    regions = [
        SfzHeaderRegion(
            value=[
                SfzOpSample(value='sample.wav'),
                SfzOpLovel(value='C3'),
                SfzOpSample(value='sample.wav'),
                SfzOpLovel(value='C3'),
            ]
        )
        for _ in range(25)
    ]
    groups = [
        SfzHeaderGroup(
            value=[*regions, SfzOpAmpegAttack('0.04'), SfzOpAmpegRelease('0.45')]
        )
        for _ in range(5)
    ]

    master = SfzHeaderMaster(value=groups)

    print(master)


if __name__ == '__main__':
    main()
