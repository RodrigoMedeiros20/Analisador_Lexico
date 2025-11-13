from enum import Enum, auto

class TokenType(Enum):
    
    # Palavras Reservadas
    MAIN = auto()       # main
    VAR = auto()        # var
    INT = auto()        # int
    REAL = auto()       # real (substitui float)
    PRINT = auto()      # print
    INPUT = auto()      # input
    IF = auto()         # if
    THEN = auto()       # then
    ELSE = auto()       # else
    WHILE = auto()      # while
    E = auto()          # E
    OU = auto()         # OU
    NAO = auto()        # NAO

    # Identificador e Literais
    IDENTIFIER = auto()
    NUMINT = auto()     # Inteiro
    NUMREAL = auto()    # Real
    CADEIA = auto()     # String

    # Operadores Aritméticos
    PLUS = auto()       # +
    MINUS = auto()      # -
    STAR = auto()       # *
    SLASH = auto()      # /
    INC = auto()        # ++
    DEC = auto()        # --

    # Operadores Relacionais (OP_REL)
    EQ = auto()         # ==
    NEQ = auto()        # !=
    GT = auto()         # >
    GTE = auto()        # >=
    LT = auto()         # <
    LTE = auto()        # <=
    
    # Operador de Atribuição
    ASSIGN_OP = auto()  # <-

    # Símbolos
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    COLON = auto()      # :
    SEMICOLON = auto()  # ;
