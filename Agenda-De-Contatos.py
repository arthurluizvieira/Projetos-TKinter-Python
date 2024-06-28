import tkinter as tk
from tkinter import messagebox

class AgendaContatos:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contatos")

        # Lista para armazenar os contatos
        self.contatos = []

        # Frame para organizar os widgets
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=10)

        # Label e entrada para o nome do contato
        self.label_nome = tk.Label(self.frame, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_nome = tk.Entry(self.frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        # Label e entrada para o telefone do contato
        self.label_telefone = tk.Label(self.frame, text="Telefone:")
        self.label_telefone.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_telefone = tk.Entry(self.frame, width=30)
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=5)

        # Botões para adicionar, remover e visualizar contatos
        self.botao_adicionar = tk.Button(self.frame, text="Adicionar", command=self.adicionar_contato)
        self.botao_adicionar.grid(row=2, column=0, padx=5, pady=10)

        self.botao_remover = tk.Button(self.frame, text="Remover", command=self.remover_contato)
        self.botao_remover.grid(row=2, column=1, padx=5, pady=10)

        self.botao_visualizar = tk.Button(self.frame, text="Visualizar Todos", command=self.visualizar_contatos)
        self.botao_visualizar.grid(row=2, column=2, padx=5, pady=10)

        # Texto para exibir os contatos
        self.texto_contatos = tk.Text(self.root, height=10, width=50)
        self.texto_contatos.pack(padx=20, pady=10)

    def adicionar_contato(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()

        if nome and telefone:
            contato = f"Nome: {nome} - Telefone: {telefone}"
            self.contatos.append(contato)
            self.entry_nome.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Contato adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def remover_contato(self):
        indice = self.texto_contatos.curselection()
        if indice:
            index = indice[0]
            contato = self.contatos[index]
            self.contatos.pop(index)
            self.atualizar_texto_contatos()
            messagebox.showinfo("Sucesso", f"Contato '{contato}' removido com sucesso.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione um contato para remover.")

    def visualizar_contatos(self):
        self.atualizar_texto_contatos()

    def atualizar_texto_contatos(self):
        self.texto_contatos.delete(1.0, tk.END)
        for contato in self.contatos:
            self.texto_contatos.insert(tk.END, contato + "\n")

# Função principal para iniciar o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    agenda_contatos = AgendaContatos(root)
    root.mainloop()
