import os

PKG_DIR = os.path.expanduser("~/.viper/packages")

def install(pkg):
    os.makedirs(PKG_DIR, exist_ok=True)
    path = os.path.join(PKG_DIR, pkg)
    with open(path, "w") as f:
        f.write(f"Package {pkg} installed")
    print(f"Installed {pkg}")

def remove(pkg):
    path = os.path.join(PKG_DIR, pkg)
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed {pkg}")
    else:
        print(f"Package {pkg} not found")

def list_packages():
    if not os.path.exists(PKG_DIR):
        print("No packages installed")
        return
    for pkg in os.listdir(PKG_DIR):
        print(pkg)
