class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self):
        self.tokens = []
        self.current_pos = 0

    def tokenize(self, input_str):
        keywords = {'DEFINE', 'END', 'IF', 'ELSE', 'WHILE'}
        operators = {'+', '-', '*', '/', '=', '=='}

        self.tokens = []
        words = input_str.split()
        for word in words:
            if word in keywords:
                self.tokens.append(Token("KEYWORD", word))
            elif word in operators:
                self.tokens.append(Token("OPERATOR", word))
            elif word.isidentifier():
                self.tokens.append(Token("IDENTIFIER", word))
            elif word.isdigit():
                self.tokens.append(Token("NUMBER", int(word)))
            else:
                raise ValueError(f"Unexpected token: {word}")

        return self.tokens
