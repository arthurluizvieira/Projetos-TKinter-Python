import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt
import os

class SistemaLoginRegistro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login e Registro")
        self.conectar_bd()

        # Definição de estilo para ttk
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))

        # Labels e Entradas para Registro
        ttk.Label(root, text="Nome de Usuário:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry_reg = ttk.Entry(root)
        self.username_entry_reg.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="Senha (mínimo 6 caracteres):").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry_reg = ttk.Entry(root, show="*")
        self.password_entry_reg.grid(row=1, column=1, padx=10, pady=10)

        self.register_btn = ttk.Button(root, text="Registrar", command=self.registrar_usuario)
        self.register_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Labels e Entradas para Login
        ttk.Label(root, text="Login - Nome de Usuário:").grid(row=3, column=0, padx=10, pady=10)
        self.username_entry_login = ttk.Entry(root)
        self.username_entry_login.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(root, text="Senha:").grid(row=4, column=0, padx=10, pady=10)
        self.password_entry_login = ttk.Entry(root, show="*")
        self.password_entry_login.grid(row=4, column=1, padx=10, pady=10)

        self.login_btn = ttk.Button(root, text="Login", command=self.realizar_login)
        self.login_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def conectar_bd(self):
        db_path = os.path.join(os.path.dirname(__file__), 'usuarios.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    def registrar_usuario(self):
        username = self.username_entry_reg.get()
        password = self.password_entry_reg.get()

        if len(password) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres.")
            return

        if username == '' or password == '':
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        # Verificar se o usuário já existe
        self.cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if self.cursor.fetchone():
            messagebox.showerror("Erro", "Nome de usuário já existe. Escolha outro.")
            return

        # Criptografar a senha antes de armazenar no banco de dados
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Inserir novo usuário no banco de dados
        self.cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()

        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso.")

    def realizar_login(self):
        username = self.username_entry_login.get()
        password = self.password_entry_login.get()

        if username == '' or password == '':
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        # Buscar usuário no banco de dados
        self.cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        usuario = self.cursor.fetchone()

        if usuario:
            # Verificar a senha
            hashed_password = usuario[2]  # A senha criptografada está na terceira coluna (índice 2)
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                messagebox.showinfo("Sucesso", "Login realizado com sucesso.")
            else:
                messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado. Faça o registro primeiro.")

    def __del__(self):
        # Fechar conexão com o banco de dados ao destruir a instância
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaLoginRegistro(root)
    root.mainloop()
