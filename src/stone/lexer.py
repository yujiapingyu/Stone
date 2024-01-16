from stone.token import Token, IdToken, NumToken, StrToken
from stone.exception import ParseException

import regex as re
import fileinput

class Lexer:
    regex_pat = r"\s*((//.*)|([0-9]+)|(\"(\\\\\"|\\\\\\\\|\\\\n|[^\"])*\")|[A-Z_a-z][A-Z_a-z0-9]*|==|<=|>=|&&|\\|\\||[\p{Symbol}\p{Punct}])?"

    def __init__(self, reader: fileinput.FileInput):
        self.pattern = re.compile(self.regex_pat)
        self.queue = []
        self.hasMore = True
        self.reader = reader

    def read(self):
        if self.fill_queue(0):
            return self.queue.pop(0)
        else:
            return Token.EOF

    def peek(self, i):
        if self.fill_queue(i):
            return self.queue[i]
        else:
            return Token.EOF

    def fill_queue(self, i):
        while i >= len(self.queue):
            if self.hasMore:
                self.readline()
            else:
                return False
        return True

    def readline(self):
        try:
            line = self.reader.readline()
        except Exception as e:
            raise ParseException('parse exception at line: {}'.format(line))

        if not line:
            self.hasMore = False
            return

        line_no = self.reader.filelineno()
        
        iter = re.finditer(self.pattern, line)
        for matcher in iter:
            self.add_token(line_no, matcher)

        self.queue.append(IdToken(line_no, Token.EOL))

    def add_token(self, line_no, matcher):
        m = matcher.group(1)
        if m and m != '':  # if not a space
            if matcher.group(2) is None:  # if not a comment
                if matcher.group(3) is not None:
                    token = NumToken(line_no, int(m))
                elif matcher.group(4) is not None:
                    token = StrToken(line_no, self.to_string_literal(m))
                else:
                    token = IdToken(line_no, m)
                self.queue.append(token)

    @staticmethod
    def to_string_literal(s):
        sb = []
        i = 1
        len_s = len(s) - 1
        while i < len_s:
            c = s[i]
            if c == '\\' and i + 1 < len_s:
                c2 = s[i + 1]
                if c2 in ['"', '\\']:
                    i += 1
                    c = s[i]
                elif c2 == 'n':
                    i += 1
                    c = '\n'
            sb.append(c)
            i += 1
        return ''.join(sb)
    
if __name__ == "__main__":
    import fileinput
    
    lexer = Lexer(fileinput.input('test.stone'))
    token = lexer.read()
    while token != Token.EOF:
        print(f"> {token.get_text()}")
        token = lexer.read()