from viper.lexer import tokenize
from viper.parser import parse

def test_parse_number():
    tokens = tokenize("123;")
    ast = parse(tokens)
    assert ast[0].node_type == "NUMBER"
