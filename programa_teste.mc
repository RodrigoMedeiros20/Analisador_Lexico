# Teste do Analisador Léxico Completo
int _var1 = 123
float var2 = .456
var2 = _var1 + 50.99

/*
  Teste de operadores
  e comentários de
  múltiplas linhas
*/
if (var2 >= 150) {
  print(var2 * 2)
} else {
  # Não faz nada
  _var1 = _var1 - 10 / 2
}

# Teste de operadores relacionais
_var1 != 100
_var1 == 98

# Erro léxico na próxima linha
@