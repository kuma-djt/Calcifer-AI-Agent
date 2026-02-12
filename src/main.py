# Calcifer entry point
from calcifer.core.runtime import Runtime

def main():
    rt = Runtime(model="gpt-5.2")
    print("Calcifer online. Type 'exit' to quit.\n")

    while True:
        user = input("> ")
        if user.strip().lower() in {"exit", "quit"}:
            break
        reply = rt.run_turn(user)
        print(f"\n{reply}\n")

if __name__ == "__main__":
    main()
