import os
from lexical.scanner import Scanner

def main():

    filename = "programa_teste.mc"
    
    if not os.path.exists(filename):
        print(f"Erro: O arquivo de teste '{filename}' não foi encontrado.")
        print("Por favor, crie o arquivo na mesma pasta do main.py.")
        return

    print(f"--- Iniciando Análise Léxica do arquivo '{filename}' ---\n")
    
    sc = Scanner(filename)
    
    tk = sc.next_token()
    while tk is not None:
        print(tk)
        tk = sc.next_token()

    print("\n--- Análise Léxica Concluída ---")

if __name__ == "__main__":
    main()