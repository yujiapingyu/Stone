class Token:
    EOF = None  # 在Python中，我们通常用None来表示特殊的或未定义的值
    EOL = "\\n"

    def __init__(self, line):
        self.lineNumber = line

    def getLineNumber(self):
        return self.lineNumber

    def isIdentifier(self):
        return False

    def isNumber(self):
        return False

    def isString(self):
        return False

    def getNumber(self):
        raise StoneException("not number token")

    def getText(self):
        return ""

# 初始化EOF为Token类的一个实例
Token.EOF = Token(-1)

class NumToken(Token):
    def __init__(self, line, value):
        super().__init__(line)
        self.value = value

    def is_number(self):
        return True

    def get_text(self):
        return str(self.value)

    def get_number(self):
        return self.value

class IdToken(Token):
    def __init__(self, line, text):
        super().__init__(line)
        self.text = text

    def is_identifier(self):
        return True

    def get_text(self):
        return self.text

class StrToken(Token):
    def __init__(self, line, literal):
        super().__init__(line)
        self.literal = literal

    def is_string(self):
        return True

    def get_text(self):
        return self.literal

