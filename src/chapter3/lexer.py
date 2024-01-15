from stone.token import Token
from stone.lexer import Lexer

if __name__ == "__main__":
    import fileinput
    
    lexer = Lexer(fileinput.input('test.stone'))
    token = lexer.read()
    while token != Token.EOF:
        print(f"> {token.get_text()}")
        token = lexer.read()