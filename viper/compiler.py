def compile_to_bytecode(ast):
    bytecode = []
    for node in ast:
        bytecode.append(("PUSH", node.value))
    return bytecode
