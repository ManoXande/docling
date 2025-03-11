# Como Executar a Interface Docling

Este documento contém instruções detalhadas sobre como executar a Interface Gráfica Docling em diferentes situações.

## Pré-requisitos

- Python 3.7 ou superior
- Tkinter (geralmente já vem com o Python)
- Biblioteca Docling

## Instalação dos Requisitos

### 1. Instalar o Docling

```bash
pip install docling
```

### 2. Verificar Tkinter (necessário apenas em alguns sistemas Linux)

No Windows e macOS, o Tkinter já vem instalado com o Python. Em sistemas Linux, você pode precisar instalá-lo:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## Opções para Executar a Interface

Existem várias formas de executar a Interface Docling:

### Opção 1: Usando o script simples (recomendado)

```bash
python start.py
```

Este é o método mais simples e direto.

### Opção 2: Usando o script de inicialização completo

```bash
python run_interface.py
```

Este script faz verificações adicionais e oferece instalar o Docling se necessário.

### Opção 3: Executando o módulo principal diretamente

```bash
python docling_interface.py
```

Executa diretamente o módulo principal da interface.

## Solução de Problemas

Se você encontrar problemas ao iniciar a interface, aqui estão algumas soluções:

### Problema: "ModuleNotFoundError: No module named 'docling'"

**Solução:** Instale o Docling:
```bash
pip install docling
```

### Problema: "ImportError: No module named 'tkinter'"

**Solução:** Instale o Tkinter conforme as instruções na seção de pré-requisitos.

### Problema: "RuntimeError: Tk não foi inicializado"

**Solução:** Isso geralmente ocorre em ambientes sem interface gráfica. Certifique-se de estar em um ambiente que suporte aplicações gráficas.

### Problema: "FileNotFoundError: [Errno 2] No such file or directory"

**Solução:** Verifique se você está executando os scripts do diretório correto, onde os arquivos estão localizados.

## Usando a Interface

1. **Selecionar uma pasta**:
   - Clique no botão "Procurar..." para selecionar uma pasta com documentos

2. **Selecionar arquivos para processamento**:
   - A lista mostrará os arquivos compatíveis na pasta
   - Selecione os arquivos que deseja processar
   - Use "Selecionar Todos" para selecionar todos os arquivos

3. **Iniciar o processamento**:
   - Clique em "Processar Arquivos Selecionados"
   - Acompanhe o progresso na barra de progresso

4. **Verificar os resultados**:
   - Ao concluir, os resultados estarão na pasta indicada em "Saída"
   - Para cada arquivo processado, serão gerados arquivos MD, HTML e JSON

## Formatos Suportados

A interface suporta o processamento dos seguintes formatos:

- PDF (`.pdf`)
- Documentos Word (`.docx`)
- Planilhas Excel (`.xlsx`)
- Apresentações PowerPoint (`.pptx`)
- HTML (`.html`)
- Texto (`.txt`)
- Imagens (`.png`, `.jpg`, `.jpeg`) 