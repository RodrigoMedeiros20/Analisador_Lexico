# RELATÓRIO: CHECKPOINT 2 - ANALISADOR SINTÁTICO

Este documento mostra o processo de implementação do Analisador Sintático (Parser) para o Checkpoint 2 da disciplina de Construção de Compiladores.

O objetivo principal foi construir um Analisador Sintático Descendente Preditivo Recursivo que valida a estrutura gramatical do código-fonte (`programa_ckp2_qui_noite.mc`), consumindo os tokens gerados pelo Analisador Léxico e seguindo a gramática fornecida (`gramatica_ckp2_qui_noite.txt`).

---

## 1. INTEGRANTES DO GRUPO

* Guilherme Medeiros
* Rennan Alves
* Rodrigo Medeiros

---

## 2. INSTRUÇÕES DE EXECUÇÃO

O projeto foi desenvolvido inteiramente em Python 3.

**Dependências:**
* Nenhuma. O projeto não requer a instalação de nenhuma biblioteca externa.

**Como Executar:**
1.  Assegure-se de que todos os arquivos e pastas (`lexical/`, `syntactic/`, `util/`, `main.py`, `programa_ckp2_qui_noite.mc`) estejam na mesma raiz.
2.  Execute o `main.py` através do terminal:
    ```bash
    python main.py
    ```
3.  O log da análise sintática aparecerá no terminal, mostrando o caminho que o analisador tomou.
4.  No final, será exibida a mensagem: `--- Análise Sintática Concluída: Nenhum erro encontrado. ---`.

**Para Testar o Tratamento de Erros:**
* Abra o arquivo `programa_ckp2_qui_noite.mc` e remova um `;` de qualquer linha.
* Rode `python main.py` novamente.
* O analisador irá parar e reportar um erro sintático claro, indicando o que era esperado e o que foi encontrado, por exemplo:

> Erro Sintático: Esperava 'SEMICOLON' mas encontrou 'input' na linha 17, coluna 5.
> --- Análise Sintática Falhou. ---

---

## 3. METODOLOGIA E DECISÕES DE PROJETO

O trabalho foi dividido em três etapas:

### 3.1. Passo 1: Adequar o Analisador Léxico

Primeiro, eu mudei o Scanner do Checkpoint 1 para que ele fosse capaz de entender a nova gramática do Checkpoint 2.

1.  **`util/token_type.py`**: O `Enum` foi atualizado para ser o dicionário completo da nova linguagem, incluindo todos os novos tokens.
2.  **`lexical/scanner.py`**: A lógica de `next_token()` foi reestruturada.
    * **Palavras-chave**: O `RESERVED_WORDS` foi atualizado.
    * **Strings**: Foi criado um novo método `_scan_string()` para lidar com literais `CADEIA` (entre aspas duplas).
    * **Números**: `_scan_number()` foi modificado para retornar `NUMINT` ou `NUMREAL` dependendo da presença do ponto decimal.
    * **Operadores**: A lógica foi reordenada para checar operadores de múltiplos caracteres (ex: `<-`, `==`, `++`) antes de seus prefixos (ex: `<`, `=`, `+`).

### 3.2. Passo 2: Criar o Analisador Descendente Preditivo Recursivo

Para a construção dos Grafos Sintáticos cada regra da gramática se tornou uma função dentro da classe `Parser`.

**A Lógica do `parser.py`:**
O parser funciona com base em três funções centrais:

1.  **`_advance()`**: É a função que "anda para frente", consumindo o token atual e pedindo o próximo ao Scanner (`self.current_token = self.scanner.next_token()`).
2.  **`_consume(expected_type)`**: É o mecanismo de validação. Ele verifica se o `self.current_token` é do tipo esperado (`expected_type`).
    * Se sim, ele chama `_advance()` para seguir em frente.
    * Se não, ele chama `_syntax_error()`, parando a análise.
3.  **`_syntax_error()`**: Ao invés de deixar o programa quebrar, esta função lança um `SyntaxError` com uma mensagem clara (linha, coluna, o que era esperado, o que foi encontrado).

**A Implementação das Regras:**
As funções de parsing (ex: `_programa`, `_corpo`, `_declaracao`) espelham a gramática.

* **Regra `"programa : 'main' '{' corpo '}'"`**
    ```python
    def _programa(self):
        self._consume(TokenType.MAIN)
        self._consume(TokenType.LBRACE)
        self._corpo() # Chamada recursiva para a próxima regra
        self._consume(TokenType.RBRACE)
    ```

* **Regras com "OU" (Ex: `"tipo : 'int' | 'real'"`)**
    Foram implementadas com `if/elif`, usando o `current_token` para prever qual caminho seguir:
    ```python
    def _tipo(self):
        if self.current_token.type == TokenType.INT:
            self._consume(TokenType.INT)
        elif self.current_token.type == TokenType.REAL:
            self._consume(TokenType.REAL)
        else:
            self._syntax_error("'int' ou 'real'")
    ```

### 3.3. Expressões e Recursão à Esquerda

A regra `"expressaoAritmetica : expressaoAritmetica '+' termo | ..."` causaria um loop infinito em um parser recursivo, pois a função `_expressaoAritmetica()` chamaria a si mesma eternamente sem consumir nenhum token.

Então removemos a recursão à esquerda reescrevendo a regra de forma iterativa.
* **Gramática Original:** `E : E '+' T | T`
* **Gramática Convertida (Iterativa):** `E : T ( '+' T )*`

Isso significa: "Uma expressão é um Termo, opcionalmente seguido por um loop de '+' e outro Termo".

**O Código (Ex: `_expressaoAritmetica`)**
```python
def _expressaoAritmetica(self):
    # 1. Analisa o primeiro 'Termo' (obrigatório)
    self._termo()
    
    # 2. Loop (para a parte 'opcional')
    while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
        self._advance() # 3. Consome o '+' ou '-'
        self._termo()   # 4. Analisa o próximo 'Termo'

Essa mesma lógica foi aplicada para _termo (com * e /) e _expressaoRelacional (com E e OU), resolvendo o problema da recursão à esquerda.

---

## 4. RESULTADO FINAL

Após a implementação de todas as regras, o parser.py está completo. Ao executar o main.py com o arquivo programa_ckp2_qui_noite.mc na pasta, o parser navega por toda a estrutura do programa, validando cada declaração, comando, if, print, atribuição e expressão.

O resultado final no console:

--- Iniciando Compilação do arquivo 'programa_ckp2_qui_noite.mc' ---
--- Iniciando Análise Sintática ---
Parsing <programa>...
Parsing <corpo>...
Parsing <secaoDeclaracoes>...
Parsing <listaDeclaracoes>...
...
... (log completo de todas as regras)
...
Parsing <comando>...
Parsing <escrita>...
Parsing <comando>...
Parsing <escrita>...
Parsing <comando>...
Parsing <escrita>...

--- Análise Sintática Concluída: Nenhum erro encontrado. ---

---

## 5. CONCLUSÃO

O projeto do Checkpoint 2 foi concluído. O Analisador Léxico foi adaptado, e um Analisador Sintático descendente recursivo foi construído. O parser é capaz de validar o código-fonte correto e reportar erros de forma clara.

---