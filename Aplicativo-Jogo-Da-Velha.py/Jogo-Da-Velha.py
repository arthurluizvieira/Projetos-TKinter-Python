import tkinter as tk
from tkinter import messagebox

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")

        self.current_player = 'X'
        self.board = [' ' for _ in range(9)]

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=' ', font=('Arial', 20), width=8, height=4,
                                   command=lambda row=i, col=j: self.click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

        reset_button = tk.Button(self.root, text="Reiniciar Jogo", command=self.reset_game)
        reset_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def click(self, row, col):
        index = 3 * row + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Fim do Jogo", f"O jogador {self.current_player} venceu!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("Fim do Jogo", "Empate!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, player):
        for combo in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def reset_game(self):
        self.current_player = 'X'
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.config(text=' ')
        messagebox.showinfo("Novo Jogo", "Jogo reiniciado!")

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()
