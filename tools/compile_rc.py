import os.path
import subprocess
import sys
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser("compile_ui")
    parser.add_argument("--src", default="./resources/resources.qrc", required=False)
    parser.add_argument("--dest", default="./resources.bin", required=False)
    parser.add_argument(
        "--exec",
        default="pyside6-rcc.exe" if sys.platform == "win32" else "pyside6-rcc",
        required=False
    )
    args = parser.parse_args()
    subprocess.check_call([args.exec, "--binary", os.path.abspath(args.src), "-o", os.path.abspath(args.dest)], cwd=os.path.abspath('.'))
