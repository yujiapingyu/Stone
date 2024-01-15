class Lexer:
    def __init__(self, reader):
        self.reader = reader
        self.last_char = None

    def get_char(self):
        if self.last_char is not None:
            c = self.last_char
            self.last_char = None
            return c
        else:
            return self.reader.read(1)

    def unget_char(self, c):
        self.last_char = c

    def read(self):
        sb = []
        c = self.get_char()
        
        if c == '':
            return None  # end of text
    
        while self.is_space(c):
            c = self.get_char()

        if self.is_digit(c):
            while self.is_digit(c):
                sb.append(c)
                c = self.get_char()
        elif self.is_letter(c):
            while self.is_letter(c) or self.is_digit(c):
                sb.append(c)
                c = self.get_char()
        elif c == '=':
            next_char = self.get_char()
            if next_char == '=':
                return '=='
            else:
                self.unget_char(next_char)
                return '='
        else:
            raise Exception('Invalid character: [{}]'.format(c))

        if c != '':
            self.unget_char(c)

        return ''.join(sb)

    @staticmethod
    def is_letter(c):
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z'

    @staticmethod
    def is_digit(c):
        return '0' <= c <= '9'

    @staticmethod
    def is_space(c):
        return 0 <= ord(c) <= ord(' ')

# 测试代码
if __name__ == '__main__':
    import io
    input_str = ' ab = 1\n b = 2 \n ab1 = 123'
    lexer = Lexer(io.StringIO(input_str))
    try:
        while True:
            token = lexer.read()
            if token is None:
                break
            print('->', token)
    except Exception as e:
        print('Error:', e)
