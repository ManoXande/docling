"""
Interface Docling

Interface gráfica para o processamento de documentos usando a biblioteca Docling.
"""

# Verificar se docling_interface está no mesmo diretório
import os
import sys
import importlib.util

try:
    # Tentar importar normalmente
    from .docling_interface import main, DoclingGUI
except (ImportError, ModuleNotFoundError):
    # Caso esteja executando diretamente do diretório, não como pacote
    current_dir = os.path.dirname(os.path.abspath(__file__))
    interface_path = os.path.join(current_dir, "docling_interface.py")
    
    if os.path.exists(interface_path):
        # Carregar dinamicamente o módulo
        spec = importlib.util.spec_from_file_location("docling_interface", interface_path)
        docling_interface = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(docling_interface)
        
        # Expor as funções e classes
        main = docling_interface.main
        DoclingGUI = docling_interface.DoclingGUI
    else:
        # Fallback: definir funções vazias para não quebrar importações
        def main():
            print("Erro: Módulo docling_interface não encontrado.")
            return 1
        
        # Classe vazia para evitar erros de importação
        class DoclingGUI:
            def __init__(self, *args, **kwargs):
                raise ImportError("Módulo docling_interface não encontrado.")

__version__ = "0.1.0"
__all__ = ["main", "DoclingGUI"] 