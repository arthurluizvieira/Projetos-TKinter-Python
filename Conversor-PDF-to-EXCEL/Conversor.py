import tkinter as tk
from tkinter import filedialog, messagebox
import tabula
import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# Função para verificar se o Java está instalado
def verificar_java():
    try:
        # Tenta chamar o comando java para verificar se está instalado
        java_check = os.system('java -version')
        if java_check == 0:
            return True
        else:
            return False
    except Exception:
        return False

class ConversorPDFExcel:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor PDF para Excel - QMOVI")

        # Verifica se o Java está instalado
        if not verificar_java():
            messagebox.showinfo("Instalar Java", "Antes de iniciar o programa, por favor, instale o Java.")
            self.root.destroy()
            return

        # Tentar definir o ícone da janela (ajustar o caminho conforme necessário)
        try:
            self.root.iconbitmap('fav-icon.ico')
        except tk.TclError as e:
            print(f"Erro ao definir o ícone da janela: {e}")

        # Frame para imagem personalizada no topo
        self.frame_topo = tk.Frame(self.root)
        self.frame_topo.pack()

        # Label para exibir imagem personalizada
        self.imagem = tk.PhotoImage(file='qmovi.png').subsample(1, 1)
        self.label_imagem = tk.Label(self.frame_topo, image=self.imagem)
        self.label_imagem.pack(pady=10)

        # Frame para seleção de arquivo
        self.frame_arquivo = tk.Frame(self.root)
        self.frame_arquivo.pack(pady=20)

        self.label_arquivo = tk.Label(self.frame_arquivo, text="Nenhum arquivo selecionado")
        self.label_arquivo.pack(padx=10, pady=10)

        self.btn_selecionar = tk.Button(self.frame_arquivo, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(padx=10, pady=10)

        # Frame para botões de ação
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack(pady=20)

        self.btn_converter = tk.Button(self.frame_botoes, text='Converter PDF para Excel', command=self.processar_pdf)
        self.btn_converter.pack(padx=10, pady=10)

        # Label para exibir resultados
        self.resultado = tk.Label(self.root, text="", fg="black")
        self.resultado.pack(pady=20)

        self.caminho_pdf = None

        # Print para verificar o caminho absoluto do ícone e da imagem
        print(f"Caminho do ícone: {os.path.abspath('fav-icon.ico')}")
        print(f"Caminho da imagem: {os.path.abspath('LogoQmoviOficial.png')}")

        # Marca d'água
        self.marca_dagua = tk.Label(self.root, text="Developed by Arthur Yokomizo", font=("Helvetica", 10, "italic"), fg="black")
        self.marca_dagua.pack(side=tk.BOTTOM, pady=10)

    def selecionar_arquivo(self):
        self.caminho_pdf = filedialog.askopenfilename(title="Selecionar PDF", filetypes=[("Arquivos PDF", "*.pdf")])
        if self.caminho_pdf:
            self.label_arquivo.config(text=f"Arquivo selecionado: {os.path.basename(self.caminho_pdf)}")
        else:
            self.label_arquivo.config(text="Nenhum arquivo selecionado")

    def processar_pdf(self):
        if not self.caminho_pdf:
            self.resultado.config(text="Nenhum arquivo PDF selecionado.", fg="red")
            return

        print(f"Caminho do PDF: {self.caminho_pdf}")  # Imprime o caminho do PDF selecionado

        try:
            # Extrair tabelas do PDF para uma lista de DataFrames do Pandas
            df_list = tabula.read_pdf(self.caminho_pdf, pages='all', multiple_tables=True, pandas_options={'header': None})

            # Concatenar todos os DataFrames em um único DataFrame se houver várias tabelas
            df_concatenado = pd.concat(df_list, ignore_index=True)

            # Diretório do arquivo de entrada
            diretorio_entrada = os.path.dirname(self.caminho_pdf)

            # Nome do arquivo de saída
            nome_base = os.path.basename(self.caminho_pdf)
            nome_base_sem_extensao = os.path.splitext(nome_base)[0]
            arquivo_saida = os.path.join(diretorio_entrada, f"{nome_base_sem_extensao}.xlsx")

            # Salvar o DataFrame em um arquivo Excel com ajuste de largura de colunas
            with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
                df_concatenado.to_excel(writer, index=False)
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']

                # Ajustar largura das colunas dinamicamente com base no conteúdo
                for col in worksheet.columns:
                    max_length = 0
                    column = col[0].column_letter  # Get the column name
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 1.2
                    worksheet.column_dimensions[column].width = 85

            self.resultado.config(text=f"Conversão concluída. Arquivo Excel salvo em '{arquivo_saida}'.", fg="green")

        except Exception as e:
            self.resultado.config(text=f"Erro ao processar o PDF: {e}", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorPDFExcel(root)
    root.mainloop()
    