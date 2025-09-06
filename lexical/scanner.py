from util.token_type import TokenType
from .token_class import Token

class Scanner:
    
    RESERVED_WORDS = {
        "int": TokenType.INT,
        "float": TokenType.FLOAT,
        "print": TokenType.PRINT,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
    }

    def __init__(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
        except IOError as e:
            print(f"Erro ao ler o arquivo: {e}")
            self.source_code = ""
        
        self.pos = 0
        self.line = 1
        self.col = 1

    def _is_eof(self) -> bool:
        return self.pos >= len(self.source_code)

    def _peek(self) -> str:
        if self._is_eof():
            return '\0'
        return self.source_code[self.pos]

    def _advance(self):
        if not self._is_eof():
            char = self.source_code[self.pos]
            if char == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    @staticmethod
    def _is_identifier_start(c: str) -> bool:
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    @staticmethod
    def _is_identifier_char(c: str) -> bool:
        return Scanner._is_identifier_start(c) or '0' <= c <= '9'

    def _scan_identifier(self) -> Token:
        start_col = self.col
        text = ""
        while self._is_identifier_char(self._peek()):
            text += self._peek()
            self._advance()
        
        token_type = self.RESERVED_WORDS.get(text, TokenType.IDENTIFIER)
        return Token(token_type, text, self.line, start_col)

    def _scan_number(self) -> Token:
        start_col = self.col
        text = ""
        while self._peek().isdigit():
            text += self._peek()
            self._advance()
        
        if self._peek() == '.':
            if self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1].isdigit():
                text += self._peek()
                self._advance()
                while self._peek().isdigit():
                    text += self._peek()
                    self._advance()
        
        return Token(TokenType.NUMBER, text, self.line, start_col)

    def next_token(self) -> Token | None:
        while not self._is_eof():
            start_col = self.col
            char = self._peek()

            if char.isspace():
                self._advance()
                continue

            if char == '#':
                while self._peek() not in ['\n', '\r', '\0']: self._advance()
                continue
            
            if char == '/' and self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1] == '*':
                self._advance(); self._advance()
                while not (self._peek() == '*' and self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1] == '/'):
                    if self._is_eof():
                        print(f"Erro Léxico: Comentário de múltiplas linhas não fechado (iniciado em {self.line}:{start_col}).")
                        return None
                    self._advance()
                self._advance(); self._advance()
                continue

            if char == '=': self._advance(); return Token(TokenType.EQ if self._match('=') else TokenType.ASSIGN, "==" if self._peek() == '=' else "=", self.line, start_col)
            if char == '!': self._advance(); return Token(TokenType.NEQ, "!=", self.line, start_col) if self._match('=') else None
            if char == '>': self._advance(); return Token(TokenType.GTE, ">=", self.line, start_col) if self._match('=') else Token(TokenType.GT, ">", self.line, start_col)
            if char == '<': self._advance(); return Token(TokenType.LTE, "<=", self.line, start_col) if self._match('=') else Token(TokenType.LT, "<", self.line, start_col)
            
            if char == '+': self._advance(); return Token(TokenType.PLUS, "+", self.line, start_col)
            if char == '-': self._advance(); return Token(TokenType.MINUS, "-", self.line, start_col)
            if char == '*': self._advance(); return Token(TokenType.STAR, "*", self.line, start_col)
            if char == '/': self._advance(); return Token(TokenType.SLASH, "/", self.line, start_col)
            if char == '(': self._advance(); return Token(TokenType.LPAREN, "(", self.line, start_col)
            if char == ')': self._advance(); return Token(TokenType.RPAREN, ")", self.line, start_col)

            if char.isdigit() or (char == '.' and self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1].isdigit()):
                return self._scan_number()

            if self._is_identifier_start(char):
                return self._scan_identifier()

            print(f"Erro Léxico: Caractere inválido '{char}' na linha {self.line}, coluna {self.col}.")
            self._advance()
            continue

        return None