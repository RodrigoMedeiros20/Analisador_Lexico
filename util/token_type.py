from enum import Enum, auto

class TokenType(Enum):
    
    # Palavras Reservadas
    INT = auto()
    FLOAT = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()

    # Identificador e Número
    IDENTIFIER = auto()
    NUMBER = auto()

    # Operadores
    PLUS = auto()           # +
    MINUS = auto()          # -
    STAR = auto()           # *
    SLASH = auto()          # /
    ASSIGN = auto()         # =
    EQ = auto()             # ==
    NEQ = auto()            # !=
    GT = auto()             # >
    GTE = auto()            # >=
    LT = auto()             # <
    LTE = auto()            # <=

    # Símbolos
    LPAREN = auto()         # (
    RPAREN = auto()         # )