from viper.runtime import core, network, dns, security

def eval_ast(ast):
    for node in ast:
        if node.node_type == "NUMBER":
            core.say(int(node.value))
        elif node.node_type == "STRING":
            core.say(node.value.strip('"'))
        elif node.node_type == "IDENT":
            if node.value == "net":
                core.say("Network module loaded")
            elif node.value == "dns":
                core.say("DNS module loaded")
            elif node.value == "security":
                core.say("Security module loaded")
