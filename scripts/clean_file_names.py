import os


def main():
    root_dir = os.path.join(os.path.dirname(__file__), "..")
    instruments_dir = os.path.abspath(os.path.join(root_dir, "instruments"))

    for path, _, files in os.walk(instruments_dir):
        if "samples" in path:
            for file in files:
                new_file_name = (
                    file.replace(" ", "_")
                    .replace("#", "s")
                    .replace(".1.", ".")
                    .strip()
                    .lower()
                )
                if "rode_nt1" in new_file_name and "rode_nt1_" not in new_file_name:
                    new_file_name = new_file_name.replace("rode_nt1", "rode_nt1_")
                if "sure_sm57" in new_file_name and "sure_sm57_" not in new_file_name:
                    new_file_name = new_file_name.replace("sure_sm57", "sure_sm57_")

                parts = os.path.join(path, file), os.path.join(path, new_file_name)
                os.rename(*parts)


if __name__ == "__main__":
    main()
