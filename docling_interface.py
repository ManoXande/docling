#!/usr/bin/env python
"""
Docling Interface
----------------
Interface gráfica para processamento de documentos usando o Docling.

Funcionalidades:
- Selecionar uma pasta no sistema de arquivos
- Criar uma subpasta para os resultados do processamento
- Visualizar e selecionar arquivos para processamento
- Processar os arquivos selecionados com o Docling
- Salvar os resultados na subpasta criada
- Feedback visual durante o processamento
- Tratamento de erros
"""

import os
import sys
import time
import threading
import tkinter as tk
import io
import tempfile
import shutil
import json
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime

# Configuração de debug
DEBUG = True

# Função para log
def debug_log(message):
    if DEBUG:
        print(f"DEBUG: {message}")

# Verificar se o Docling está instalado
try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    # Não vamos sair imediatamente para permitir que o módulo seja importado
    DocumentConverter = None


class DoclingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Docling Interface")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Verificar Docling na inicialização da GUI
        if not DOCLING_AVAILABLE:
            messagebox.showerror("Erro", "A biblioteca Docling não está instalada. Instale usando: pip install docling")
            self.root.destroy()
            return
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5)
        self.style.configure("TFrame", padding=10)
        self.style.configure("TLabel", padding=5)
        
        # Variáveis
        self.selected_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.status_text = tk.StringVar(value="Pronto para começar")
        self.processing = False
        self.files_to_process = []
        self.temp_files = []  # Lista para manter arquivos temporários
        self.manual_mode = tk.BooleanVar(value=False)  # Modo manual para processamento direto
        self.save_json = tk.BooleanVar(value=True)     # Opção para salvar JSON
        self.save_html = tk.BooleanVar(value=True)     # Opção para salvar HTML
        self.save_md = tk.BooleanVar(value=True)       # Opção para salvar MD
        
        # Definir extensões suportadas - garantir que .txt esteja incluído e que todos os formatos tenham ponto
        self.supported_extensions = [
            '.txt',  # Texto
            '.pdf',  # PDF
            '.docx', # Word
            '.xlsx', # Excel
            '.html', # HTML
            '.pptx', # PowerPoint
            '.png',  # Imagem PNG
            '.jpg',  # Imagem JPG
            '.jpeg'  # Imagem JPEG
        ]
        
        # Extensões que o Docling suporta diretamente (sem pré-processamento)
        self.docling_native_extensions = [
            '.pdf',
            '.docx',
            '.xlsx',
            '.html',
            '.pptx',
            '.png',
            '.jpg',
            '.jpeg'
        ]
        
        # Criar o conversor Docling
        try:
            self.converter = DocumentConverter()
        except Exception as e:
            messagebox.showerror("Erro na inicialização do Docling", f"Erro: {str(e)}")
            self.root.destroy()
            return
        
        # Construir a interface
        self._create_widgets()
        
    def _create_widgets(self):
        """Criar todos os widgets da interface."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior para seleção de pasta
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, expand=False, pady=5)
        
        ttk.Label(folder_frame, text="Pasta:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(folder_frame, textvariable=self.selected_folder, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(folder_frame, text="Procurar...", command=self._browse_folder).pack(side=tk.LEFT, padx=5)
        
        # Frame para o output
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, expand=False, pady=5)
        
        ttk.Label(output_frame, text="Saída:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(output_frame, textvariable=self.output_folder, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Opções
        options_frame = ttk.LabelFrame(main_frame, text="Opções")
        options_frame.pack(fill=tk.X, expand=False, pady=5)
        
        # Checkbox para modo manual
        ttk.Checkbutton(
            options_frame, 
            text="Processamento direto (ignorar pré-processamento)",
            variable=self.manual_mode
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Frame para as opções de formatos de saída
        format_frame = ttk.LabelFrame(main_frame, text="Formatos de Saída")
        format_frame.pack(fill=tk.X, expand=False, pady=5)
        
        # Checkbox para cada formato
        ttk.Checkbutton(
            format_frame, 
            text="Markdown (.md)",
            variable=self.save_md
        ).pack(side=tk.LEFT, padx=15, pady=5)
        
        ttk.Checkbutton(
            format_frame, 
            text="HTML (.html)",
            variable=self.save_html
        ).pack(side=tk.LEFT, padx=15, pady=5)
        
        ttk.Checkbutton(
            format_frame, 
            text="JSON (.json)",
            variable=self.save_json
        ).pack(side=tk.LEFT, padx=15, pady=5)
        
        # Frame para a lista de arquivos
        files_frame = ttk.LabelFrame(main_frame, text="Arquivos Disponíveis")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Lista de arquivos com scrollbar
        self.file_listbox_frame = ttk.Frame(files_frame)
        self.file_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(self.file_listbox_frame, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.file_listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botões de ação
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, expand=False, pady=10)
        
        ttk.Button(buttons_frame, text="Selecionar Todos", command=self._select_all_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Limpar Seleção", command=self._clear_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Atualizar Lista", command=lambda: self._update_file_list(self.selected_folder.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Listar Todos Arquivos", command=self._list_all_files).pack(side=tk.LEFT, padx=5)
        
        # Botão de processamento
        self.process_button = ttk.Button(
            buttons_frame, 
            text="Processar Arquivos Selecionados", 
            command=self._process_selected_files
        )
        self.process_button.pack(side=tk.RIGHT, padx=5)
        
        # Barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, expand=False, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, expand=False)
        
        ttk.Label(status_frame, textvariable=self.status_text).pack(fill=tk.X, padx=5)
        
    def _browse_folder(self):
        """Abrir diálogo para seleção de pasta."""
        folder = filedialog.askdirectory(title="Selecione uma pasta")
        if folder:
            self.selected_folder.set(folder)
            debug_log(f"Pasta selecionada: {folder}")
            
            # Criar subpasta para resultados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join(folder, f"docling_results_{timestamp}")
            self.output_folder.set(output_dir)
            
            # Atualizar lista de arquivos
            self._update_file_list(folder)
    
    def _list_all_files(self):
        """Listar todos os arquivos na pasta selecionada para diagnóstico."""
        folder = self.selected_folder.get()
        if not folder:
            messagebox.showinfo("Informação", "Selecione uma pasta primeiro")
            return
            
        try:
            # Limpar listbox
            self.file_listbox.delete(0, tk.END)
            self.files_to_process = []
            
            all_files = []
            all_extensions = set()
            
            # Listar todos os arquivos na pasta selecionada
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, folder)
                    _, ext = os.path.splitext(file.lower())
                    
                    # Adicionar à lista de todos os arquivos
                    all_files.append((rel_path, file_path, ext))
                    if ext:
                        all_extensions.add(ext)
            
            # Mostrar todos os arquivos encontrados
            for rel_path, file_path, ext in all_files:
                self.file_listbox.insert(tk.END, f"{rel_path} [{ext}]")
            
            # Mostrar informações sobre os arquivos encontrados
            messagebox.showinfo(
                "Todos os Arquivos", 
                f"Encontrados {len(all_files)} arquivos na pasta.\n"
                f"Extensões encontradas: {', '.join(sorted(all_extensions))}\n"
                f"Extensões suportadas: {', '.join(self.supported_extensions)}\n"
                f"Extensões suportadas pelo Docling: {', '.join(self.docling_native_extensions)}"
            )
            
            self.status_text.set(f"Listados todos os {len(all_files)} arquivos na pasta")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar arquivos: {str(e)}")
    
    def _update_file_list(self, folder):
        """Atualizar a lista de arquivos baseado na pasta selecionada."""
        if not folder:
            return
            
        debug_log(f"Atualizando lista de arquivos da pasta: {folder}")
        
        self.file_listbox.delete(0, tk.END)
        self.files_to_process = []
        
        try:
            # Verificar se a pasta existe
            if not os.path.exists(folder):
                self.status_text.set(f"Pasta não encontrada: {folder}")
                return
                
            # Contador para debug
            count_by_ext = {ext: 0 for ext in self.supported_extensions}
            total_files = 0
            compatible_files = 0
            
            # Buscar arquivos na pasta e subpastas
            for root, _, files in os.walk(folder):
                for file in files:
                    total_files += 1
                    
                    # Obter extensão em minúsculas e garantir que tenha o ponto
                    filename, ext = os.path.splitext(file)
                    ext = ext.lower()
                    if ext and not ext.startswith('.'):
                        ext = '.' + ext
                    
                    debug_log(f"Arquivo encontrado: {file} com extensão: {ext}")
                    
                    # Verificar se é uma extensão suportada
                    if ext in self.supported_extensions:
                        debug_log(f"Arquivo compatível: {file}")
                        compatible_files += 1
                        
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, folder)
                        
                        # Verificar se é uma extensão nativa do Docling ou precisará de pré-processamento
                        needs_preprocessing = ext not in self.docling_native_extensions
                        
                        # Armazenar o caminho e flag de pré-processamento
                        self.files_to_process.append((rel_path, file_path, needs_preprocessing))
                        
                        # Adicionar indicação visual de pré-processamento na lista
                        if needs_preprocessing:
                            self.file_listbox.insert(tk.END, f"{rel_path} [Requer pré-processamento]")
                        else:
                            self.file_listbox.insert(tk.END, rel_path)
                        
                        # Incrementar contador da extensão
                        count_by_ext[ext] += 1
            
            debug_log(f"Total de arquivos: {total_files}, Compatíveis: {compatible_files}")
            debug_log(f"Contagem por extensão: {count_by_ext}")
            
            # Mensagem de status com informações detalhadas
            if self.files_to_process:
                # Criar texto com contagem por extensão
                ext_counts = [f"{count} {ext}" for ext, count in count_by_ext.items() if count > 0]
                ext_text = ", ".join(ext_counts)
                self.status_text.set(f"Encontrados {len(self.files_to_process)} arquivos compatíveis: {ext_text}")
                
                # Verificar se há arquivos TXT que precisam de pré-processamento
                txt_files = count_by_ext.get('.txt', 0)
                if txt_files > 0:
                    messagebox.showinfo(
                        "Informação sobre Arquivos TXT", 
                        f"Foram encontrados {txt_files} arquivos .txt que requerem pré-processamento.\n\n"
                        "Estes arquivos serão convertidos para HTML antes do processamento pelo Docling.\n"
                        "Se preferir processá-los diretamente, marque a opção 'Processamento direto'."
                    )
            else:
                self.status_text.set("Nenhum arquivo compatível encontrado na pasta")
                
                # Mostrar mensagem mais detalhada
                messagebox.showinfo(
                    "Informação", 
                    f"Nenhum arquivo compatível encontrado na pasta selecionada.\n\n"
                    f"Total de arquivos encontrados: {total_files}\n"
                    f"Extensões suportadas: {', '.join(self.supported_extensions)}\n\n"
                    f"Use o botão 'Listar Todos Arquivos' para ver todos os arquivos disponíveis."
                )
                
        except Exception as e:
            debug_log(f"Erro ao listar arquivos: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao listar arquivos: {str(e)}")
            self.status_text.set(f"Erro ao listar arquivos: {str(e)}")
    
    def _select_all_files(self):
        """Selecionar todos os arquivos na lista."""
        if self.file_listbox.size() > 0:
            self.file_listbox.select_set(0, tk.END)
        else:
            messagebox.showinfo("Informação", "Não há arquivos para selecionar")
    
    def _clear_selection(self):
        """Limpar a seleção de arquivos."""
        self.file_listbox.selection_clear(0, tk.END)
    
    def _preprocess_txt_file(self, file_path):
        """
        Converte arquivos TXT para HTML para processamento pelo Docling.
        Retorna o caminho do arquivo HTML temporário.
        """
        try:
            debug_log(f"Pré-processando arquivo TXT: {file_path}")
            
            # Criar nome para arquivo temporário
            temp_dir = tempfile.gettempdir()
            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]
            temp_html_path = os.path.join(temp_dir, f"{base_name}_{int(time.time())}.html")
            
            # Ler o conteúdo do arquivo TXT
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Converter para HTML simples
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{file_name}</title>
</head>
<body>
    <pre>{content}</pre>
</body>
</html>
"""
            
            # Salvar como HTML
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Adicionar à lista de arquivos temporários para limpeza posterior
            self.temp_files.append(temp_html_path)
            
            debug_log(f"Arquivo TXT convertido para HTML: {temp_html_path}")
            return temp_html_path
            
        except Exception as e:
            debug_log(f"Erro ao pré-processar arquivo TXT: {str(e)}")
            raise Exception(f"Erro ao pré-processar arquivo TXT: {str(e)}")
    
    def _create_custom_json(self, file_path, content):
        """
        Cria um JSON personalizado com base no conteúdo do arquivo original.
        """
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            
            # Criar um dicionário com informações úteis
            data = {
                "file_info": {
                    "name": file_name,
                    "path": file_path,
                    "size_bytes": file_size,
                    "last_modified": datetime.fromtimestamp(mod_time).isoformat(),
                    "format": "text/plain"
                },
                "content": {
                    "text": content,
                    "length": len(content),
                    "lines": content.count('\n') + 1
                },
                "metadata": {
                    "processed_by": "Docling Interface",
                    "processed_at": datetime.now().isoformat(),
                    "encoding": "utf-8"
                }
            }
            
            # Converter para JSON formatado
            return json.dumps(data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            debug_log(f"Erro ao criar JSON personalizado: {str(e)}")
            return json.dumps({"error": str(e)})
    
    def _process_selected_files(self):
        """Iniciar processamento dos arquivos selecionados."""
        selected_indices = self.file_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado")
            return
        
        if not self.selected_folder.get():
            messagebox.showwarning("Aviso", "Selecione uma pasta primeiro")
            return
        
        # Verificar se pelo menos um formato de saída está selecionado
        if not any([self.save_md.get(), self.save_html.get(), self.save_json.get()]):
            messagebox.showwarning("Aviso", "Selecione pelo menos um formato de saída (MD, HTML ou JSON)")
            return
        
        # Limpar lista de arquivos temporários
        self.temp_files = []
        
        # Criar diretório de saída se não existir
        output_dir = self.output_folder.get()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar pasta de saída: {str(e)}")
            return
        
        # Obter arquivos selecionados
        selected_files = [self.files_to_process[i] for i in selected_indices]
        
        # Verificar se há arquivos TXT que precisam de pré-processamento
        has_txt_files = any(needs_preprocessing for _, _, needs_preprocessing in selected_files)
        
        # Avisar sobre o pré-processamento de arquivos TXT se não estiver em modo manual
        if has_txt_files and not self.manual_mode.get():
            txt_count = sum(1 for _, _, needs_preprocessing in selected_files if needs_preprocessing)
            messagebox.showinfo(
                "Pré-processamento de Arquivos TXT",
                f"{txt_count} arquivos TXT serão pré-processados para HTML antes do processamento.\n"
                "Este processo pode demorar um pouco dependendo do tamanho dos arquivos."
            )
        
        # Iniciar processamento em thread separada
        self.processing = True
        self.process_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(selected_files)
        
        processing_thread = threading.Thread(
            target=self._process_files_thread,
            args=(selected_files, output_dir)
        )
        processing_thread.daemon = True
        processing_thread.start()
    
    def _process_files_thread(self, files, output_dir):
        """Processar arquivos em uma thread separada."""
        successful = 0
        failed = 0
        
        for i, (rel_path, file_path, needs_preprocessing) in enumerate(files):
            try:
                # Atualizar interface para o arquivo atual
                self.root.after(
                    0, 
                    lambda msg=f"Processando ({i+1}/{len(files)}): {rel_path}": self.status_text.set(msg)
                )
                
                debug_log(f"Processando arquivo: {file_path}")
                
                # Ler o conteúdo original para caso seja necessário criar um JSON personalizado
                original_content = ""
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        original_content = f.read()
                except Exception as e:
                    debug_log(f"Não foi possível ler o conteúdo original: {str(e)}")
                
                # Verificar se precisa de pré-processamento e não está em modo manual
                actual_file_path = file_path
                needs_custom_json = False
                
                if needs_preprocessing and not self.manual_mode.get():
                    self.root.after(
                        0, 
                        lambda msg=f"Pré-processando ({i+1}/{len(files)}): {rel_path}": self.status_text.set(msg)
                    )
                    try:
                        actual_file_path = self._preprocess_txt_file(file_path)
                        debug_log(f"Usando arquivo pré-processado: {actual_file_path}")
                        needs_custom_json = True  # Arquivos TXT precisarão de JSON personalizado
                    except Exception as e:
                        debug_log(f"Erro no pré-processamento, usando arquivo original: {str(e)}")
                        # Continuar com o arquivo original se o pré-processamento falhar
                        actual_file_path = file_path
                
                # Processar o arquivo
                result = self.converter.convert(actual_file_path)
                doc = result.document
                
                # Criar subdiretório se necessário
                file_dir = os.path.dirname(rel_path)
                if file_dir:
                    out_subdir = os.path.join(output_dir, file_dir)
                    os.makedirs(out_subdir, exist_ok=True)
                
                # Obter nome base do arquivo
                base_name = Path(file_path).stem
                output_base = os.path.join(output_dir, os.path.dirname(rel_path), base_name)
                
                # Salvar em diferentes formatos conforme selecionado pelo usuário
                if self.save_md.get():
                    try:
                        # Markdown
                        markdown = doc.export_to_markdown()
                        with open(f"{output_base}.md", "w", encoding="utf-8") as f:
                            f.write(markdown or "")
                        debug_log(f"Markdown salvo: {output_base}.md")
                    except Exception as e:
                        debug_log(f"Erro ao exportar markdown: {str(e)}")
                        self.root.after(0, lambda e=e: self._log_error(f"Erro ao exportar markdown: {str(e)}"))
                
                if self.save_html.get():
                    try:
                        # HTML
                        html_output = getattr(doc, 'export_to_html', lambda: "")()
                        with open(f"{output_base}.html", "w", encoding="utf-8") as f:
                            f.write(html_output or "")
                        debug_log(f"HTML salvo: {output_base}.html")
                    except Exception as e:
                        debug_log(f"Erro ao exportar HTML: {str(e)}")
                        self.root.after(0, lambda e=e: self._log_error(f"Erro ao exportar HTML: {str(e)}"))
                
                if self.save_json.get():
                    try:
                        # JSON - verificar se precisa criar um JSON personalizado
                        if needs_custom_json and original_content:
                            # Criar JSON personalizado para arquivos TXT
                            json_output = self._create_custom_json(file_path, original_content)
                        else:
                            # Usar o JSON gerado pelo Docling
                            json_output = getattr(doc, 'export_to_json', lambda: "{}")()
                            
                            # Verificar se o JSON está vazio ou é inválido
                            if not json_output or json_output == "{}" or json_output == "null":
                                # Fallback para JSON personalizado se o conteúdo original estiver disponível
                                if original_content:
                                    json_output = self._create_custom_json(file_path, original_content)
                        
                        with open(f"{output_base}.json", "w", encoding="utf-8") as f:
                            f.write(json_output or "{}")
                        debug_log(f"JSON salvo: {output_base}.json")
                    except Exception as e:
                        debug_log(f"Erro ao exportar JSON: {str(e)}")
                        self.root.after(0, lambda e=e: self._log_error(f"Erro ao exportar JSON: {str(e)}"))
                
                successful += 1
            except Exception as e:
                failed += 1
                debug_log(f"Erro ao processar {rel_path}: {str(e)}")
                self.root.after(0, lambda e=e: self._log_error(f"Erro ao processar {rel_path}: {str(e)}"))
            
            # Atualizar barra de progresso
            self.root.after(0, lambda: self.progress_bar.step())
        
        # Limpar arquivos temporários
        try:
            for temp_file in self.temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    debug_log(f"Arquivo temporário removido: {temp_file}")
        except Exception as e:
            debug_log(f"Erro ao limpar arquivos temporários: {str(e)}")
        
        # Processamento concluído
        self.root.after(0, lambda: self._processing_completed(successful, failed, output_dir))
    
    def _log_error(self, message):
        """Registrar um erro no console e na interface."""
        print(f"ERRO: {message}", file=sys.stderr)
        self.status_text.set(f"ERRO: {message}")
    
    def _processing_completed(self, successful, failed, output_dir):
        """Callback para quando o processamento estiver completo."""
        self.processing = False
        self.process_button.config(state=tk.NORMAL)
        
        message = f"Processamento concluído. Sucesso: {successful}, Falhas: {failed}"
        self.status_text.set(message)
        
        if successful > 0:
            messagebox.showinfo(
                "Processamento Concluído", 
                f"{message}\n\nResultados salvos em:\n{output_dir}"
            )
        else:
            messagebox.showerror(
                "Processamento Falhou", 
                f"Nenhum arquivo foi processado com sucesso. Verifique os erros."
            )


def main():
    """Função principal para executar a aplicação."""
    # Verificar se o Docling está disponível antes de iniciar a interface
    if not DOCLING_AVAILABLE and __name__ == "__main__":
        print("Erro: A biblioteca Docling não está instalada.")
        print("Por favor, instale usando: pip install docling")
        return 1
    
    try:
        root = tk.Tk()
        app = DoclingGUI(root)
        root.mainloop()
        return 0
    except Exception as e:
        # Se for uma exceção relacionada ao Tkinter, mostrar no console
        print(f"Erro ao iniciar a aplicação: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 