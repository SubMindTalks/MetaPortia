from typing import List, Tuple
import re

class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

class Lexer:
    def __init__(self):
        self.tokens = []
        
    def tokenize(self, source: str) -> List[Token]:
        """Convert source code into tokens."""
        # Implementation here
        pass