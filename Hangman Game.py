import random
import tkinter as tk
from tkinter import messagebox

difficulty_level = {
    'easy': 10,
    'medium': 7,
    'hard': 5
}


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.word = ""
        self.display_word = ""
        self.remaining_letters = 0
        self.count_wrong = 0
        self.guessed_letters = ""
        self.difficulty = "easy"
        self.wrong_guesses = 0

        self.create_interface()

    def create_interface(self):
        self.top_frame = tk.Frame(self.root, bg='black')
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        self.game_title = tk.Label(
            self.top_frame, bg='black', fg='white', text='Hangman Game', font=('', 24)
        )
        self.game_title.pack(pady=10)

        self.word_label = tk.Label(self.top_frame, bg='black', fg='white', text='', font=('', 18))
        self.word_label.pack(pady=10)

        self.info_label = tk.Label(self.top_frame, bg='black', fg='white', text='', font=('', 14))
        self.info_label.pack(pady=10)

        self.entry_frame = tk.Frame(self.root, bg='black')
        self.entry_frame.pack(fill=tk.BOTH, expand=True)

        self.letter_entry = tk.Entry(self.entry_frame, font=('', 18))
        self.letter_entry.pack(pady=10)

        self.guess_button = tk.Button(
            self.entry_frame, text="Guess", command=self.make_guess, font=('', 18)
        )
        self.guess_button.pack(pady=10)

        self.difficulty_frame = tk.Frame(self.root, bg='black')
        self.difficulty_frame.pack(fill=tk.BOTH, expand=True)

        self.create_difficulty_buttons()

    def create_difficulty_buttons(self):
        difficulties = ["Easy", "Medium", "Hard"]
        for difficulty in difficulties:
            button = tk.Button(
                self.difficulty_frame, text=difficulty, command=lambda d=difficulty: self.set_difficulty(d),
                font=('', 14)
            )
            button.pack(side=tk.LEFT, padx=10)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty.lower()
        self.wrong_guesses = difficulty_level[self.difficulty]
        self.reset_game()

    def reset_game(self):
        self.word = self.get_random_word()
        self.display_word = "_" * len(self.word)
        self.remaining_letters = len(self.word)
        self.count_wrong = 0
        self.guessed_letters = ""

        self.update_display()

    def get_random_word(self):
        try:
            with open("words.txt", "r") as file:
                words = file.read().splitlines()
                return random.choice(words).upper()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            self.root.quit()

    def update_display(self):
        self.word_label.config(text=" ".join(self.display_word))
        self.info_label.config(
            text=f"Wrong guesses: {self.count_wrong}\nGuessed letters: {', '.join(self.guessed_letters)}"
        )

    def make_guess(self):
        guess = self.letter_entry.get().strip().upper()
        self.letter_entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1 or guess in self.guessed_letters:
            messagebox.showwarning("Invalid Input", "Please enter a valid letter.")
            return

        self.guessed_letters += guess

        if guess in self.word:
            self.display_word = "".join(
                [letter if letter in self.guessed_letters else "_" for letter in self.word]
            )
            self.remaining_letters = self.display_word.count("_")
        else:
            self.count_wrong += 1

        self.update_display()

        if self.remaining_letters == 0:
            messagebox.showinfo("Congratulations!", f"You win! The word was {self.word}")
            self.reset_game()
        elif self.count_wrong >= self.wrong_guesses:
            messagebox.showinfo("Game Over", f"You lost! The word was {self.word}")
            self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
