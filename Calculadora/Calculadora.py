import tkinter as tk

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Básica")

        # Cria uma string variável para armazenar os números e a expressão
        self.expression = tk.StringVar()
        self.expression.set("")

        # Caixa de entrada para exibir a expressão
        self.display = tk.Entry(root, font=('Arial', 18, 'bold'), textvariable=self.expression, bd=5, insertwidth=4, width=25, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Botões numéricos e operações
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 4, 1)  # Botão 'C' para limpar a expressão
        ]

        for (text, row, column) in buttons:
            tk.Button(root, text=text, font=('Arial', 14, 'bold'), command=lambda t=text: self.click(t)).grid(row=row, column=column, padx=5, pady=5)

    def click(self, value):
        if value == '=':
            # Calcular o resultado da expressão
            try:
                result = str(eval(self.expression.get()))
                self.expression.set(result)
            except:
                self.expression.set("Erro")
        elif value == 'C':
            # Limpar a expressão
            self.clear_expression()
        else:
            # Atualizar a expressão com o valor do botão clicado
            self.expression.set(self.expression.get() + value)

    def clear_expression(self):
        self.expression.set("")  # Define a expressão como vazia

# Função principal para iniciar a calculadora
if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculadora(root)
    root.mainloop()
