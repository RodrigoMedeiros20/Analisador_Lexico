from lexical.scanner import Scanner
from util.token_type import TokenType
from lexical.token_class import Token

class Parser:
    
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_token: Token = None
        self._advance()

    def _advance(self):
        """Consome o token atual e pega o próximo do scanner."""
        self.current_token = self.scanner.next_token()

    def _consume(self, expected_type: TokenType):
        """
        Verifica e consome o token atual.
        Se o token não for o esperado, lança um erro sintático.
        """
        if self.current_token and self.current_token.type == expected_type:
            self._advance()
        else:
            self._syntax_error(expected_type)

    def _syntax_error(self, expected: TokenType | str):
        """Helper para reportar erros de forma padronizada."""
        expected_str = expected.name if isinstance(expected, TokenType) else expected
        
        if self.current_token:
            raise SyntaxError(
                f"Erro Sintático: Esperava '{expected_str}' mas encontrou '{self.current_token.text}' "
                f"na linha {self.current_token.line}, coluna {self.current_token.col}."
            )
        else:
            raise SyntaxError(
                f"Erro Sintático: Esperava '{expected_str}' mas encontrou o Fim de Arquivo."
            )

    # --- Ponto de Entrada da Análise ---
    
    def parse(self):
        """Inicia a análise sintática a partir da regra inicial 'programa'."""
        print("--- Iniciando Análise Sintática ---")
        try:
            self._programa()
            
            # Requisito: Após _programa() terminar, não deve haver mais tokens
            if self.current_token is not None:
                raise SyntaxError(
                    f"Erro Sintático: Token inesperado '{self.current_token.text}' "
                    f"após o fim do programa na linha {self.current_token.line}."
                )
            
            # Requisito 2: Compilar sem erros o programa de teste
            print("\n--- Análise Sintática Concluída: Nenhum erro encontrado. ---")
            
        except SyntaxError as e:
            # Requisito 3: Reportar erros sintáticos
            print(f"\n{e}")
            print("--- Análise Sintática Falhou. ---")
            
    # --- Implementação das Regras da Gramática ---

    def _programa(self):
        """Regra: programa : 'main' '{' corpo '}'"""
        print("Parsing <programa>...")
        self._consume(TokenType.MAIN)
        self._consume(TokenType.LBRACE)
        self._corpo()
        self._consume(TokenType.RBRACE)

    def _corpo(self):
        """Regra: corpo : secaoDeclaracoes listaComandos"""
        print("Parsing <corpo>...")
        self._secaoDeclaracoes()
        self._listaComandos() 

    def _secaoDeclaracoes(self):
        """Regra: secaoDeclaracoes : 'var' '{' listaDeclaracoes '}'"""
        print("Parsing <secaoDeclaracoes>...")
        self._consume(TokenType.VAR)
        self._consume(TokenType.LBRACE)
        self._listaDeclaracoes()
        self._consume(TokenType.RBRACE)

    def _listaDeclaracoes(self):
        """Regra: listaDeclaracoes : (declaracao)+"""
        print("Parsing <listaDeclaracoes>...")
        # A gramática exige pelo menos uma declaração
        self._declaracao()
        # Continua parsando declarações (que começam com ID)
        while self.current_token and self.current_token.type == TokenType.ID:
            self._declaracao()

    def _declaracao(self):
        """Regra: declaracao : ID ':' tipo ';'"""
        print("Parsing <declaracao>...")
        self._consume(TokenType.ID)
        self._consume(TokenType.COLON)
        self._tipo()
        self._consume(TokenType.SEMICOLON)

    def _tipo(self):
        """Regra: tipo : 'int' | 'real'"""
        print("Parsing <tipo>...")
        if self.current_token and self.current_token.type == TokenType.INT:
            self._consume(TokenType.INT)
        elif self.current_token and self.current_token.type == TokenType.REAL:
            self._consume(TokenType.REAL)
        else:
            self._syntax_error("'int' ou 'real'")
            
    def _listaComandos(self):
        """Regra: listaComandos : (comando)+"""
        print("Parsing <listaComandos>...")
        # A gramática exige pelo menos um comando
        self._comando()
        
        # Continua parsando enquanto o token atual for o início de um comando
        # FIRST(comando) = {ID, INPUT, PRINT, IF, WHILE, LBRACE}
        while self.current_token and self.current_token.type in (
            TokenType.ID, TokenType.INPUT, TokenType.PRINT,
            TokenType.IF, TokenType.WHILE, TokenType.LBRACE
        ):
            self._comando()

    def _comando(self):
        """Regra: comando : atribuicao | leitura | escrita | condicional | repeticao | bloco"""
        print("Parsing <comando>...")
        if not self.current_token:
            self._syntax_error("um comando (ID, input, print, if, while, {)")

        if self.current_token.type == TokenType.ID:
            self._atribuicao()
        elif self.current_token.type == TokenType.INPUT:
            self._leitura()
        elif self.current_token.type == TokenType.PRINT:
            self._escrita()
        elif self.current_token.type == TokenType.IF:
            self._condicional() # Agora implementado
        elif self.current_token.type == TokenType.WHILE:
            self._repeticao() # Agora implementado
        elif self.current_token.type == TokenType.LBRACE:
            self._bloco()
        else:
            self._syntax_error("o início de um comando (ID, input, print, if, while, {)")
    
    def _atribuicao(self):
        """Regra: atribuicao : ID '<-' expressaoAritmetica ';';"""
        print("Parsing <atribuicao>...")
        self._consume(TokenType.ID)
        self._consume(TokenType.ASSIGN_OP)
        self._expressaoAritmetica()
        self._consume(TokenType.SEMICOLON)

    def _leitura(self):
        """Regra: leitura : 'input(' ID ')' ';';"""
        print("Parsing <leitura>...")
        self._consume(TokenType.INPUT)
        self._consume(TokenType.LPAREN)
        self._consume(TokenType.ID)
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)

    def _escrita(self):
        """Regra: escrita : 'print(' (ID | CADEIA) ')' ';';"""
        print("Parsing <escrita>...")
        self._consume(TokenType.PRINT)
        self._consume(TokenType.LPAREN)
        if self.current_token and self.current_token.type == TokenType.ID:
            self._consume(TokenType.ID)
        elif self.current_token and self.current_token.type == TokenType.CADEIA:
            self._consume(TokenType.CADEIA)
        else:
            self._syntax_error("ID ou CADEIA")
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
    
    # --- NOVO e COMPLETO ---
    def _condicional(self):
        """
        Regra:
        condicional :
            'if' expressaoRelacional 'then' comando |
            'if' expressaoRelacional 'then' comando 'else' comando;
        """
        print("Parsing <condicional>...")
        self._consume(TokenType.IF)
        self._expressaoRelacional()
        self._consume(TokenType.THEN)
        self._comando() # O comando do 'then'
        
        # Verifica se existe um 'else' opcional
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self._consume(TokenType.ELSE)
            self._comando() # O comando do 'else'

    # --- NOVO e COMPLETO ---
    def _repeticao(self):
        """
        Regra:
        repeticao : 'while' expressaoRelacional comando;
        """
        print("Parsing <repeticao>...")
        self._consume(TokenType.WHILE)
        self._expressaoRelacional()
        self._comando()

    def _bloco(self):
        """Regra: bloco : '{' listaComandos '}'"""
        print("Parsing <bloco>...")
        self._consume(TokenType.LBRACE)
        self._listaComandos()
        self._consume(TokenType.RBRACE)

    # --- Expressões Aritméticas ---
    
    def _expressaoAritmetica(self):
        """Regra (Iterativa): expressaoAritmetica : termo (('+' | '-') termo)*"""
        print("Parsing <expressaoAritmetica>...")
        self._termo()
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            self._advance() # Consome o '+' ou '-'
            self._termo()

    def _termo(self):
        """Regra (Iterativa): termo : fator (('*' | '/') fator)*"""
        print("Parsing <termo>...")
        self._fator()
        while self.current_token and self.current_token.type in (TokenType.STAR, TokenType.SLASH):
            self._advance() # Consome o '*' ou '/'
            self._fator()

    def _fator(self):
        """
        Regra:
        fator :
            NUMINT | NUMREAL | ID |
            '(' expressaoAritmetica ')' |
            ID '++' | ID '--';
        """
        print("Parsing <fator>...")
        if not self.current_token:
            self._syntax_error("um fator (NUMINT, NUMREAL, ID, '(')")

        if self.current_token.type == TokenType.NUMINT:
            self._consume(TokenType.NUMINT)
        elif self.current_token.type == TokenType.NUMREAL:
            self._consume(TokenType.NUMREAL)
        elif self.current_token.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            self._expressaoAritmetica()
            self._consume(TokenType.RPAREN)
        elif self.current_token.type == TokenType.ID:
            self._consume(TokenType.ID) # Consome o ID
            if self.current_token and self.current_token.type == TokenType.INC:
                self._consume(TokenType.INC) # É ID '++'
            elif self.current_token and self.current_token.type == TokenType.DEC:
                self._consume(TokenType.DEC) # É ID '--'
            # Se não, era apenas 'ID'
        else:
            self._syntax_error("um fator (NUMINT, NUMREAL, ID, '(')")

    # --- Expressões Relacionais (NOVAS) ---

    def _expressaoRelacional(self):
        """
        Regra (Iterativa):
        expressaoRelacional : termoRelacional (operadorLogico termoRelacional)*
        """
        print("Parsing <expressaoRelacional>...")
        self._termoRelacional()
        
        # Loop (exp_rel_linha): consome ('E', 'OU', 'NAO') e o próximo termo
        while self.current_token and self.current_token.type in (
            TokenType.E, TokenType.OU, TokenType.NAO
        ):
            self._operadorLogico()
            self._termoRelacional()

    def _termoRelacional(self):
        """
        Regra:
        termoRelacional :
            expressaoAritmetica OP_REL expressaoAritmetica |
            '(' expressaoRelacional ')'
        """
        print("Parsing <termoRelacional>...")
        if not self.current_token:
            self._syntax_error("uma expressão relacional ('(', ID, num, ...)")

        # Checa se é uma (expressaoRelacional)
        if self.current_token.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            self._expressaoRelacional()
            self._consume(TokenType.RPAREN)
            return # Terminou essa regra

        # Se não, deve ser: expressaoAritmetica OP_REL expressaoAritmetica
        # FIRST(expressaoAritmetica) = {NUMINT, NUMREAL, '(', ID}
        # Como já tratamos '(', o resto deve ser uma expressão aritmética
        self._expressaoAritmetica()
        
        # Agora, consome o Operador Relacional (OP_REL)
        if self.current_token and self.current_token.type in (
            TokenType.EQ, TokenType.NEQ, TokenType.GT,
            TokenType.GTE, TokenType.LT, TokenType.LTE
        ):
            self._advance() # Consome o OP_REL (==, !=, >, >=, <, <=)
        else:
            self._syntax_error("um operador relacional (==, !=, >, <, ...)")
            
        # Finalmente, consome a segunda expressão aritmética
        self._expressaoAritmetica()

    def _operadorLogico(self):
        """
        Regra:
        operadorLogico : 'E' | 'OU' | 'NAO'
        """
        print("Parsing <operadorLogico>...")
        if self.current_token and self.current_token.type == TokenType.E:
            self._consume(TokenType.E)
        elif self.current_token and self.current_token.type == TokenType.OU:
            self._consume(TokenType.OU)
        elif self.current_token and self.current_token.type == TokenType.NAO:
            self._consume(TokenType.NAO)
        else:
            self._syntax_error("'E', 'OU' ou 'NAO'")