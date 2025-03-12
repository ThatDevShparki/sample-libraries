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
                # skip chords ... for now
                if "chord" in file:
                    # print(file)
                    if "flat" not in file:
                        mic_name, mic_serial, key, _, volume = file.split(".")[0].split(
                            "_"
                        )
                else:
                    mic_name, mic_serial, key, volume = file.split(".")[0].split("_")

                mic = "_".join([mic_name, mic_serial])
                key = key.replace("s", "#").lower().strip()

                print(f"<region> sample={os.path.join('./samples', file)} key={key}")


if __name__ == "__main__":
    main()
