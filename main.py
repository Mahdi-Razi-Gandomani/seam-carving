import sys
from cli import run_cli

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Run with arguments, e.g.: python3 main.py input.jpg output.jpg --vertical 20 --gif")
    else:
        run_cli()
