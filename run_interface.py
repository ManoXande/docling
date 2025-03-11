#!/usr/bin/env python
"""
Script para executar a Interface Docling
----------------------------------------

Este script é uma forma simples de iniciar a interface gráfica Docling.

Uso:
  python run_interface.py
"""

import sys
import os
import traceback

# Verificar a versão do Python
if sys.version_info < (3, 7):
    print("Erro: Python 3.7 ou superior é necessário para executar esta aplicação.")
    sys.exit(1)

# Tentar importar o tkinter
try:
    import tkinter as tk
except ImportError:
    print("Erro: Tkinter não está disponível. Este é um requisito para a interface gráfica.")
    print("Em sistemas Linux, você pode instalar com:")
    print("  sudo apt-get install python3-tk  # Para Ubuntu/Debian")
    print("  sudo dnf install python3-tkinter # Para Fedora")
    sys.exit(1)

# Verificar se o Docling está instalado e oferecer instalação
docling_installed = False
try:
    import docling
    docling_installed = True
except ImportError:
    print("Aviso: A biblioteca Docling não foi encontrada.")
    install = input("Deseja instalar o Docling agora? (s/n): ")
    if install.lower() in ('s', 'sim', 'y', 'yes'):
        try:
            import subprocess
            print("Instalando Docling...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "docling"])
            print("Docling instalado com sucesso!")
            docling_installed = True
        except Exception as e:
            print(f"Erro ao instalar Docling: {e}")
            print("Por favor, instale manualmente usando: pip install docling")
            sys.exit(1)
    else:
        print("A aplicação requer o Docling. Por favor, instale-o com: pip install docling")
        sys.exit(1)

# Adicionar o diretório atual ao path para garantir que o módulo seja encontrado
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Importar e executar a interface
try:
    # Tentar importar diretamente
    try:
        from docling_interface import main
        main()
    except ImportError:
        # Se não conseguir importar diretamente, tentar importar do arquivo
        interface_path = os.path.join(current_dir, "docling_interface.py")
        if os.path.exists(interface_path):
            print("Importando módulo diretamente do arquivo...")
            import importlib.util
            spec = importlib.util.spec_from_file_location("docling_interface", interface_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.main()
        else:
            print(f"Erro: Arquivo docling_interface.py não encontrado em {current_dir}")
            sys.exit(1)
except KeyboardInterrupt:
    print("\nAplicação interrompida pelo usuário.")
    sys.exit(0)
except Exception as e:
    print(f"Erro ao iniciar a interface: {e}")
    print("\nInformações de diagnóstico:")
    traceback.print_exc()
    sys.exit(1) 