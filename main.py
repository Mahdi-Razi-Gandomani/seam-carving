import sys
from cli import run_cli

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Run with arguments -> python3 main.py input.jpg output.jpg --vertical 20")
        sys.exit(1)
    else:
        run_cli()
