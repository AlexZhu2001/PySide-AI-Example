import sys
import subprocess
from pathlib import Path
from argparse import ArgumentParser


def is_ui_files(fn: str | Path):
    return str(fn).lower().endswith(".ui")


def compile_ui(ui_src_folder: str | Path, ui_dest_folder: str | Path, uic_exec="pyside6-uic"):
    src = (
        Path(ui_src_folder)
        if isinstance(ui_src_folder, str) else ui_src_folder
    )
    dest = (
        Path(ui_dest_folder)
        if isinstance(ui_dest_folder, str) else ui_dest_folder
    )
    for root, _, files in src.walk():
        ui_files = filter(is_ui_files, files)
        relative_path = root.relative_to(src)
        dest_path = dest.joinpath(relative_path)
        dest_path.mkdir(parents=True, exist_ok=True)
        init_file = dest_path.joinpath("__init__.py")
        if not init_file.exists():
            init_file.touch()
        for f in ui_files:
            input_fp = Path(root).joinpath(f)
            output_fn = '.'.join(str(f).split('.')[:-1]) + ".py"
            output_fp = dest_path.joinpath(output_fn)
            subprocess.check_call([uic_exec, input_fp, "-o", output_fp])


if __name__ == "__main__":
    parser = ArgumentParser("compile_ui")
    parser.add_argument("--ui_src", default="./ui_src", required=False)
    parser.add_argument("--ui_dest", default="./ui", required=False)
    parser.add_argument(
        "--uic_exec",
        default="pyside6-uic.exe" if sys.platform == "win32" else "pyside6-uic",
        required=False
    )
    args = parser.parse_args()
    compile_ui(args.ui_src, args.ui_dest, args.uic_exec)
