from runner import run_engine

def main():
    print("=== ULTIMATE ENGINE ===")
    print(run_engine("ultimate", {"msg": "ping"}))

    print("\n=== TENET ENGINE ===")
    print(run_engine("tenet", {"msg": "ping"}))

    print("\n=== ENGINE-365-DAYS ===")
    print(run_engine("worker365", {"msg": "ping"}))

    print("\n=== TRON ENGINE ===")
    print(run_engine("tron", {"n": 3029}))

    print("\n=== ZHA ENGINE ===")
    print(run_engine("zha", {"msg": "ping"}))

    print("\n=== XYO ENGINE ===")
    print(run_engine("xyo", {"msg": "ping"}))

if __name__ == "__main__":
    main()
