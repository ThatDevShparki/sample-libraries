import os


def main():
    root_dir = os.path.join(os.path.dirname(__file__), "..")
    instruments_dir = os.path.abspath(os.path.join(root_dir, "instruments"))

    instrument_paths = []
    for path, folders, files in os.walk(instruments_dir):
        if "samples" in folders and any(".sfz" in f for f in files):
            instrument_paths.append(path)

    for instrument_path in instrument_paths:
        for _, _, files in os.walk(os.path.join(instrument_path, "samples")):
            for file in files:
                if "chord" in file:
                    if "flat" in file:
                        continue

                    mic_name, mic_serial, key, _, volume = file.split(".")[0].split("_")
                    key = key + "1"
                else:
                    mic_name, mic_serial, key, volume = file.split(".")[0].split("_")

                mic = "_".join([mic_name, mic_serial])

                lowvel, hivel = 0, 0
                if volume == "low":
                    lowvel, hivel = 1, 42
                elif volume == "med":
                    lowvel, hivel = 43, 85
                else:
                    lowvel, hivel = 86, 127

                key = key.replace("s", "#").lower().strip()

                print(
                    f"<region> sample={os.path.join('./samples', file)} key={key} lowvel={str(lowvel)} hivel={str(hivel)}"
                )


if __name__ == "__main__":
    main()
