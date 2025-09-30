from viper.lexer import tokenize

def test_numbers():
    assert tokenize("123;")[0][0] == "NUMBER"
