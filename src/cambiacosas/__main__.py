import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python -m cambiacosas <arg1> <arg2>")
        sys.exit(1)

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    # --- Your tool's logic will go here ---
    print(f"Argument 1: {arg1}")
    print(f"Argument 2: {arg2}")
    print("Tool logic to be implemented...")
    # --- End of tool's logic ---

if __name__ == "__main__":
    main()