# Interface Gráfica Docling

Uma interface gráfica para processamento de documentos usando a biblioteca [Docling](https://ds4sd.github.io/docling/).

![Docling Interface](https://ds4sd.github.io/docling/assets/docling_processing.png)

## Funcionalidades

- Seleção de pasta contendo documentos a serem processados
- Criação automática de subpasta para armazenar resultados
- Visualização e seleção de arquivos a serem processados
- Processamento em segundo plano com feedback visual (barra de progresso)
- Exportação dos resultados em múltiplos formatos (Markdown, HTML, JSON)
- Tratamento de erros e feedback visual
- Suporte a múltiplos formatos de documento

## Formatos Suportados

- PDF (`.pdf`)
- Documentos Word (`.docx`)
- Planilhas Excel (`.xlsx`)
- Apresentações PowerPoint (`.pptx`)
- Páginas HTML (`.html`)
- Arquivos de texto (`.txt`)
- Imagens (`.png`, `.jpg`, `.jpeg`)

## Pré-requisitos

- Python 3.7+
- Tkinter (geralmente já vem com o Python)
- Biblioteca Docling

## Instalação

### 1. Instalar a biblioteca Docling

```bash
pip install docling
```

### 2. Executar a interface

```bash
# Diretamente do arquivo python
python docling_interface.py
```

## Guia de Uso

1. **Iniciar a aplicação**:
   - Execute o script `docling_interface.py`

2. **Selecionar uma pasta**:
   - Clique no botão "Procurar..." para selecionar uma pasta contendo os documentos
   - A aplicação automaticamente criará uma subpasta para os resultados

3. **Selecionar arquivos para processamento**:
   - A lista de arquivos compatíveis será exibida
   - Selecione os arquivos que deseja processar:
     - Clique em um arquivo para selecioná-lo
     - Ctrl+Clique para selecionar vários arquivos
     - Use o botão "Selecionar Todos" para selecionar todos os arquivos

4. **Processar os arquivos**:
   - Clique em "Processar Arquivos Selecionados"
   - A barra de progresso indicará o andamento do processamento
   - O status atual será exibido abaixo da barra de progresso

5. **Resultados**:
   - Ao concluir, uma mensagem será exibida com o resumo do processamento
   - Os resultados serão salvos na pasta indicada no campo "Saída"
   - Para cada arquivo processado, serão gerados 3 arquivos:
     - `.md` (formato Markdown)
     - `.html` (formato HTML)
     - `.json` (formato JSON para uso programático)

## Tratamento de Erros

A interface inclui diversas verificações e tratamento de erros:

- Verificação se a biblioteca Docling está instalada
- Validação da seleção de pasta e arquivos
- Tratamento de exceções durante o processamento
- Feedback visual de erros

## Desenvolvimento

Para contribuir com o desenvolvimento:

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install docling
   ```
3. Execute a aplicação:
   ```bash
   python docling_interface.py
   ```

## Créditos

- [Docling](https://ds4sd.github.io/docling/) - Biblioteca para processamento de documentos
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Biblioteca gráfica padrão do Python
