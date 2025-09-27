import sys
import math
import random
import os

GLOBAL_NS = {
    "math": math,
    "random": random,
}

VIPER_FUNCTIONS = {}

def viper_func(fn):
    VIPER_FUNCTIONS[fn.__name__] = fn
    GLOBAL_NS[fn.__name__] = fn
    return fn

@viper_func
def vip_print(*args):
    print(*args)

@viper_func
def vip_add(a, b):
    return a + b

def import_viper_module(module_name):
    path = f"{module_name}.vmod"
    if not os.path.exists(path):
        print(f"모듈을 찾을 수 없습니다: {module_name}")
        return
    with open(path, "r", encoding="utf-8") as f:
        run_code(f.read())

def run_code(code: str):
    try:
        result = eval(code, GLOBAL_NS)
        if result is not None:
            print(result)
    except SyntaxError:
        try:
            exec(code, GLOBAL_NS)
        except Exception as e:
            print("에러:", e)
    except Exception as e:
        print("에러:", e)

def show_help():
    print("=== Viper Lite Help ===")
    print("REPL 명령어: exit, help, manual, import [모듈명]")
    print("Viper 함수:", ', '.join(VIPER_FUNCTIONS.keys()))
    print("Python 라이브러리: math, random 등 GLOBAL_NS 참조")

def show_manual():
    print("🐍=== Viper Lite Mini 매뉴얼 ===🐍")
    print("REPL 명령어: exit, help, manual, import [모듈명]")
    print("Viper 함수:", ', '.join(VIPER_FUNCTIONS.keys()))
    print("Python 라이브러리: math, random 등 GLOBAL_NS 참조")
    print("예시:")
    print(">>> vip_print('안녕')")
    print(">>> vip_add(3,5)")
    print(">>> math.sqrt(16)")
    print(">>> import mymodule")
    print(">>> exit")

def repl():
    print("🐍 Viper Lite REPL (manual 입력 가능)")
    while True:
        try:
            code = input(">>> ").strip()
            if code.lower() == "exit":
                print("REPL 종료")
                break
            elif code.lower() == "help":
                show_help()
            elif code.lower() == "manual":
                show_manual()
            elif code.startswith("import "):
                import_viper_module(code.split()[1])
            else:
                run_code(code)
        except KeyboardInterrupt:
            print("\n(REPL 강제 종료)")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                run_code(f.read())
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다:", filename)
    else:
        repl()
