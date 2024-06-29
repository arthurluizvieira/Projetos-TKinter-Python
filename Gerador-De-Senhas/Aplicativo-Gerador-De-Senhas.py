import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class GeradorSenhasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Senhas Seguras")

        self.comprimento_label = ttk.Label(root, text="Comprimento da Senha:")
        self.comprimento_label.pack(pady=10)

        self.comprimento_entry = ttk.Entry(root)
        self.comprimento_entry.pack()

        self.check_letras_maiusculas = tk.BooleanVar()
        self.check_letras_maiusculas.set(True)
        self.check_letras_maiusculas_cb = ttk.Checkbutton(root, text="Incluir letras maiúsculas", variable=self.check_letras_maiusculas)
        self.check_letras_maiusculas_cb.pack()

        self.check_letras_minusculas = tk.BooleanVar()
        self.check_letras_minusculas.set(True)
        self.check_letras_minusculas_cb = ttk.Checkbutton(root, text="Incluir letras minúsculas", variable=self.check_letras_minusculas)
        self.check_letras_minusculas_cb.pack()

        self.check_numeros = tk.BooleanVar()
        self.check_numeros.set(True)
        self.check_numeros_cb = ttk.Checkbutton(root, text="Incluir números", variable=self.check_numeros)
        self.check_numeros_cb.pack()

        self.check_simbolos = tk.BooleanVar()
        self.check_simbolos.set(False)
        self.check_simbolos_cb = ttk.Checkbutton(root, text="Incluir símbolos", variable=self.check_simbolos)
        self.check_simbolos_cb.pack()

        self.gerar_btn = ttk.Button(root, text="Gerar Senha", command=self.gerar_senha)
        self.gerar_btn.pack(pady=20)

        self.senha_label = ttk.Label(root, text="")
        self.senha_label.pack(pady=10)

    def gerar_senha(self):
        comprimento = int(self.comprimento_entry.get())

        if comprimento <= 0:
            messagebox.showerror("Erro", "O comprimento da senha deve ser maior que zero.")
            return

        caracteres = ""

        if self.check_letras_maiusculas.get():
            caracteres += string.ascii_uppercase

        if self.check_letras_minusculas.get():
            caracteres += string.ascii_lowercase

        if self.check_numeros.get():
            caracteres += string.digits

        if self.check_simbolos.get():
            caracteres += string.punctuation

        if caracteres == "":
            messagebox.showerror("Erro", "Selecione pelo menos um tipo de caractere para incluir na senha.")
            return

        senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
        self.senha_label.config(text=f"Senha gerada: {senha}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorSenhasApp(root)
    root.mainloop()
