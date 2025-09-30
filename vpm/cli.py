import sys
from .registry import install_package

def main():
    if len(sys.argv) < 3:
        print("Usage: vpm install <package>")
        return
    command, package = sys.argv[1], sys.argv[2]
    if command == "install":
        install_package(package)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
