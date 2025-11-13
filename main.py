import os
from lexical.scanner import Scanner
from syntactic.parser import Parser # Importa o Parser

def main():

    filename = "programa_ckp2_qui_noite.mc"
    
    if not os.path.exists(filename):
        print(f"Erro: O arquivo de teste '{filename}' não foi encontrado.")
        return

    print(f"--- Iniciando Compilação do arquivo '{filename}' ---")
    
    try:
        # 1. Análise Léxica (O Parser gerencia o Scanner)
        sc = Scanner(filename)
        
        # 2. Análise Sintática (Inicia o processo)
        parser = Parser(sc)
        parser.parse() # Chama o ponto de entrada do parser

    except SyntaxError as e:
        # Pega erros sintáticos reportados pelo Parser
        print(f"Erro de Compilação: {e}")
    except Exception as e:
        # Pega outros erros (ex: arquivo não encontrado)
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()