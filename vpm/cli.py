import sys
from . import registry, utils

def main():
    if len(sys.argv) < 2:
        print("Usage: vpm [install|remove|list] <package>")
        return

    cmd = sys.argv[1]
    if cmd == "install":
        pkg = sys.argv[2]
        registry.install(pkg)
    elif cmd == "remove":
        pkg = sys.argv[2]
        registry.remove(pkg)
    elif cmd == "list":
        registry.list_packages()
    else:
        print("Unknown command:", cmd)
