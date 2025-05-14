import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.player_name = simpledialog.askstring("Player Name", "Enter your name:", parent=self.root)
        if not self.player_name:
            self.player_name = "Player"

        self.board = [' '] * 9
        self.buttons = []
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.winning_combo = []

        self.create_widgets()
        self.computer_first_move()

    def create_widgets(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=('Arial', 14))
        self.score_label.grid(row=0, column=0, columnspan=3, pady=5)

        for i in range(9):
            btn = tk.Button(self.root, text=' ', font=('Arial', 20), width=5, height=2,
                            command=lambda i=i: self.user_move(i))
            btn.grid(row=(i // 3) + 1, column=i % 3)
            self.buttons.append(btn)

        self.reset_button = tk.Button(self.root, text="Restart Game", font=('Arial', 12), command=self.reset_game)
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

    def get_score_text(self):
        return f"{self.player_name} (O): {self.player_score}  |  Computer (X): {self.computer_score}  |  Ties: {self.tie_score}"

    def update_score(self):
        self.score_label.config(text=self.get_score_text())

    def reset_game(self):
        self.board = [' '] * 9
        self.winning_combo = []
        for btn in self.buttons:
            btn.config(text=' ', state=tk.NORMAL, bg='SystemButtonFace')
        self.computer_first_move()

    def computer_first_move(self):
        self.make_move(4, 'X')
        self.buttons[4].config(state=tk.DISABLED)

    def user_move(self, index):
        if self.board[index] == ' ':
            self.make_move(index, 'O')
            if self.check_game_over('O'):
                return
            self.root.after(400, self.computer_move)

    def computer_move(self):
        available = [i for i in range(9) if self.board[i] == ' ']
        if available:
            move = random.choice(available)
            self.make_move(move, 'X')
            self.check_game_over('X')

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state=tk.DISABLED)

    def check_game_over(self, player):
        win = self.check_win(player)
        if win:
            self.winning_combo = win
            self.animate_winning_line()

            if player == 'O':
                self.player_score += 1
                messagebox.showinfo("Game Over", f"{self.player_name} wins! 🎉")
            else:
                self.computer_score += 1
                messagebox.showinfo("Game Over", "Computer wins! 🤖")

            self.end_game()
            return True
        elif ' ' not in self.board:
            self.tie_score += 1
            messagebox.showinfo("Game Over", "It's a tie!")
            self.end_game()
            return True
        return False

    def end_game(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.update_score()

    def check_win(self, player):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combo in combos:
            if all(self.board[i] == player for i in combo):
                return combo
        return None

    def animate_winning_line(self, count=0):
        if count < 6:
            color = 'lightgreen' if count % 2 == 0 else 'yellow'
            for i in self.winning_combo:
                self.buttons[i].config(bg=color)
            self.root.after(300, lambda: self.animate_winning_line(count + 1))
        else:
            # Final color after flashing
            for i in self.winning_combo:
                self.buttons[i].config(bg='lightgreen')

# Run the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
