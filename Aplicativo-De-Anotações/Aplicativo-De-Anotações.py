import tkinter as tk
from tkinter import Menu, scrolledtext, filedialog, messagebox
import os

class AplicativoAnotacoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de Anotações")

        # Configuração da área de texto
        self.txt_area = scrolledtext.ScrolledText(root, width=60, height=15)
        self.txt_area.pack(pady=10)

        # Configuração do menu
        self.menu = Menu(root)
        self.root.config(menu=self.menu)

        # Menu Arquivo
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Nova Nota", command=self.nova_nota)
        self.file_menu.add_command(label="Abrir Nota", command=self.abrir_nota)
        self.file_menu.add_command(label="Salvar Nota", command=self.salvar_nota)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.sair_aplicativo)

        # Menu Editar
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Editar Nota", command=self.editar_nota)
        self.edit_menu.add_command(label="Excluir Nota", command=self.excluir_nota)

        # Caminho do arquivo atual
        self.arquivo_atual = None

    def nova_nota(self):
        self.txt_area.delete(1.0, tk.END)
        self.arquivo_atual = None

    def abrir_nota(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if arquivo:
            try:
                with open(arquivo, 'r') as f:
                    conteudo = f.read()
                    self.txt_area.delete(1.0, tk.END)
                    self.txt_area.insert(tk.END, conteudo)
                    self.arquivo_atual = arquivo
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir arquivo: {str(e)}")

    def salvar_nota(self):
        if self.arquivo_atual:
            try:
                with open(self.arquivo_atual, 'w') as f:
                    texto = self.txt_area.get(1.0, tk.END)
                    f.write(texto)
                messagebox.showinfo("Sucesso", "Nota salva com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar nota: {str(e)}")
        else:
            self.salvar_como()

    def salvar_como(self):
        try:
            arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
            if arquivo:
                with open(arquivo, 'w') as f:
                    texto = self.txt_area.get(1.0, tk.END)
                    f.write(texto)
                self.arquivo_atual = arquivo
                messagebox.showinfo("Sucesso", "Nota salva com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar nota: {str(e)}")

    def editar_nota(self):
        if not self.arquivo_atual:
            messagebox.showwarning("Aviso", "Nenhuma nota aberta para editar.")
            return
        self.txt_area.config(state=tk.NORMAL)

    def excluir_nota(self):
        if self.arquivo_atual and os.path.exists(self.arquivo_atual):
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta nota?")
            if resposta:
                try:
                    os.remove(self.arquivo_atual)
                    self.txt_area.delete(1.0, tk.END)
                    self.arquivo_atual = None
                    messagebox.showinfo("Sucesso", "Nota excluída com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir nota: {str(e)}")
        else:
            messagebox.showwarning("Aviso", "Nenhuma nota aberta para excluir.")

    def sair_aplicativo(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoAnotacoes(root)
    root.mainloop()
