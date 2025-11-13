from util.token_type import TokenType
from .token_class import Token

class Scanner:
    
    # Dicionário atualizado para o Checkpoint 2
    RESERVED_WORDS = {
        "main": TokenType.MAIN,
        "var": TokenType.VAR,
        "int": TokenType.INT,
        "real": TokenType.REAL,
        "print": TokenType.PRINT,
        "input": TokenType.INPUT,
        "if": TokenType.IF,
        "then": TokenType.THEN,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "E": TokenType.E,
        "OU": TokenType.OU,
        "NAO": TokenType.NAO,
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

    # --- Métodos de Controle ---
    
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
        if self._is_eof():
            return False
        if self.source_code[self.pos] != expected:
            return False
        
        # Avança a coluna antes de avançar a posição
        # (self._advance() cuidará da linha se for '\n', mas aqui não será)
        self.col += 1
        self.pos += 1
        return True

    # --- Métodos de Reconhecimento (Scanning) ---

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
        
        # Verifica se é uma palavra reservada ou um identificador
        token_type = self.RESERVED_WORDS.get(text, TokenType.ID)
        return Token(token_type, text, self.line, start_col)

    def _scan_number(self) -> Token:
        start_col = self.col
        text = ""
        token_type = TokenType.NUMINT # Assume inteiro por padrão

        # Caso especial: número começando com '.' (ex: .456)
        if self._peek() == '.':
            token_type = TokenType.NUMREAL
            text += self._peek()
            self._advance()
            while self._peek().isdigit():
                text += self._peek()
                self._advance()
            return Token(token_type, text, self.line, start_col)

        # Caso normal: número começando com dígito (ex: 123 ou 123.45)
        while self._peek().isdigit():
            text += self._peek()
            self._advance()
        
        if self._peek() == '.':
            # Verifica se tem dígito DEPOIS do ponto
            if self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1].isdigit():
                token_type = TokenType.NUMREAL # Vira real
                text += self._peek()
                self._advance()
                while self._peek().isdigit():
                    text += self._peek()
                    self._advance()
            # Se for "123." (sem dígito depois), será um NUMINT 123
            # e o '.' será pego na próxima iteração do next_token (dando erro)
        
        return Token(token_type, text, self.line, start_col)
    
    def _scan_string(self) -> Token:
        start_col = self.col
        start_line = self.line
        self._advance() # Consome o " inicial
        text = ""
        
        while self._peek() != '"':
            if self._is_eof():
                print(f"Erro Léxico: String não finalizada (iniciada em {start_line}:{start_col}).")
                return None
            
            # A gramática não parece suportar strings com quebra de linha
            if self._peek() == '\n':
                 print(f"Erro Léxico: Quebra de linha inesperada dentro da string (iniciada em {start_line}:{start_col}).")
                 return None
            
            text += self._peek()
            self._advance()
        
        self._advance() # Consome o " final
        return Token(TokenType.CADEIA, text, start_line, start_col)

    # --- Método Principal ---

    def next_token(self) -> Token | None:
        while not self._is_eof():
            start_col = self.col
            char = self._peek()

            # 1. Ignorar Espaços em Branco
            if char.isspace():
                self._advance()
                continue

            # 2. Ignorar Comentários
            # Comentário de linha única
            if char == '#':
                while self._peek() not in ['\n', '\r', '\0']:
                    self._advance()
                continue
            
            # Comentário de múltiplas linhas
            if char == '/' and self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1] == '*':
                self._advance(); self._advance() # Consome /*
                while not (self._peek() == '*' and self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1] == '/'):
                    if self._is_eof():
                        print(f"Erro Léxico: Comentário de múltiplas linhas não fechado (iniciado em {self.line}:{start_col}).")
                        return None
                    self._advance()
                self._advance(); self._advance() # Consome */
                continue

            # 3. Operadores de Múltiplos Caracteres (devem ser checados antes dos de um)

            # = ou ==
            if char == '=':
                self._advance()
                if self._match('='):
                    return Token(TokenType.EQ, "==", self.line, start_col)
                else:
                    # '=' (atribuição simples) não existe mais nesta gramática
                    print(f"Erro Léxico: Operador de atribuição inválido '=' na linha {self.line}, coluna {self.col}. (Use '<-' para atribuição)")
                    continue
            
            # !=
            if char == '!':
                self._advance()
                if self._match('='):
                    return Token(TokenType.NEQ, "!=", self.line, start_col)
                else:
                    # '!' sozinho não é válido
                    print(f"Erro Léxico: Caractere inválido '!' na linha {self.line}, coluna {self.col}. ('!' deve ser seguido de '=')")
                    continue

            # > ou >=
            if char == '>':
                self._advance()
                return Token(TokenType.GTE, ">=", self.line, start_col) if self._match('=') else Token(TokenType.GT, ">", self.line, start_col)

            # <, <=, ou <-
            if char == '<':
                self._advance()
                if self._match('='):
                    return Token(TokenType.LTE, "<=", self.line, start_col)
                elif self._match('-'):
                    return Token(TokenType.ASSIGN_OP, "<-", self.line, start_col)
                else:
                    return Token(TokenType.LT, "<", self.line, start_col)
            
            # + ou ++
            if char == '+':
                self._advance()
                return Token(TokenType.INC, "++", self.line, start_col) if self._match('+') else Token(TokenType.PLUS, "+", self.line, start_col)
            
            # - ou --
            if char == '-':
                self._advance()
                return Token(TokenType.DEC, "--", self.line, start_col) if self._match('-') else Token(TokenType.MINUS, "-", self.line, start_col)

            # 4. Símbolos de Um Caractere
            if char == '*': self._advance(); return Token(TokenType.STAR, "*", self.line, start_col)
            if char == '/': self._advance(); return Token(TokenType.SLASH, "/", self.line, start_col) # '/*
            if char == '(': self._advance(); return Token(TokenType.LPAREN, "(", self.line, start_col)
            if char == ')': self._advance(); return Token(TokenType.RPAREN, ")", self.line, start_col)
            if char == '{': self._advance(); return Token(TokenType.LBRACE, "{", self.line, start_col)
            if char == '}': self._advance(); return Token(TokenType.RBRACE, "}", self.line, start_col)
            if char == ':': self._advance(); return Token(TokenType.COLON, ":", self.line, start_col)
            if char == ';': self._advance(); return Token(TokenType.SEMICOLON, ";", self.line, start_col)

            # 5. Literais (String, Número)
            
            # String (CADEIA)
            if char == '"':
                return self._scan_string()

            # Número (NUMINT ou NUMREAL)
            # (Verifica se é dígito OU se é '.' seguido de dígito)
            if char.isdigit() or (char == '.' and self.pos + 1 < len(self.source_code) and self.source_code[self.pos + 1].isdigit()):
                return self._scan_number()

            # 6. Identificadores e Palavras-chave
            if self._is_identifier_start(char):
                return self._scan_identifier()

            # 7. Erro
            print(f"Erro Léxico: Caractere inválido '{char}' na linha {self.line}, coluna {self.col}.")
            self._advance()
            continue

        return None