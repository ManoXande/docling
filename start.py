#!/usr/bin/env python
"""
Inicializador simples para a Interface Docling
---------------------------------------------

Um script mínimo para executar a interface Docling.
"""

if __name__ == "__main__":
    try:
        # Tentar importar diretamente do arquivo
        from docling_interface import main
        main()
    except ImportError:
        # Se falhar, tentar executar o script de inicialização completo
        print("Usando inicializador alternativo...")
        import run_interface 