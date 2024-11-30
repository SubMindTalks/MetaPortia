class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        return self.statements()

    def statements(self):
        statements = []
        while self.current_token and self.current_token.type != "END":
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == "KEYWORD" and self.current_token.value == "DEFINE":
            return self.define_statement()
        raise ValueError(f"Unexpected token: {self.current_token}")

    def define_statement(self):
        self.advance()  # Skip DEFINE
        var_name = self.current_token.value
        self.advance()
        if self.current_token.value != "=":
            raise ValueError("Expected '=' after variable name")
        self.advance()  # Skip '='
        value = self.current_token.value
        self.advance()  # Skip value
        return {"type": "DEFINE", "var_name": var_name, "value": value}
