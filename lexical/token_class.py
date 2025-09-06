from dataclasses import dataclass
from util.token_type import TokenType

@dataclass
class Token:
    
    type: TokenType
    text: str
    line: int
    col: int

    def __str__(self):
        return f"Token [type={self.type.name}, text='{self.text}', line={self.line}, col={self.col}]"