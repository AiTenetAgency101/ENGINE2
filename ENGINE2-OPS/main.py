import sys
from ops.runner import run

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py tron_cycle <4digit>")
        raise SystemExit(1)

    op_name = sys.argv[1]
    n = int(sys.argv[2])
    record = run(op_name, {"n": n})
    print(record)

if __name__ == "__main__":
    main()
