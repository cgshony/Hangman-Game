"""Implementation of the classic  word-guessing Hangman game. The player
tries to guess a hidden word, letter by letter. """

import random

def get_random_word():
    """Pick a random word from a list of words"""
    try:
        with open("words.txt", "r") as file:
            words = file.read().splitlines()
            return random.choice(words).upper()
    except FileNotFoundError:
        print("File not found.")
        return None

def user_interface(count_wrong, count_guesses, guessed_letters, display_word):
    """Display the basic game interface."""
    print("\nHangman Game!")
    print("Word:", display_word)
    print("Wrong guesses:", count_wrong)
    print("Guessed letters:", guessed_letters)

def play_game():
    """Main game logic."""
    word = get_random_word()
    word_length = len(word)
    remaining_letters = word_length
    display_word = "_" * word_length
    count_wrong = 0
    count_guesses = 0
    guessed_letters = ""

    user_interface(count_wrong, count_guesses, guessed_letters, display_word)

    while count_wrong < 10 and remaining_letters > 0:
        guess = get_letter(guessed_letters) #Get letter from the player and concatenate it to the guessed letters
        guessed_letters += guess

        if guess in word:
            display_word = ""
            remaining_letters = word_length

            for letter in word:
                if letter in guessed_letters:
                    display_word += letter
                    remaining_letters -= 1
                else:
                    display_word += "_"
        else:
            count_wrong += 1

        count_guesses += 1

        user_interface(count_wrong, count_guesses, guessed_letters, display_word)

    if remaining_letters == 0:
        print("Congratulations! You win in", count_guesses, "guesses")
    else:
        print("You lost! The word was:", word)

def get_letter(guessed_letters):
    """Get a valid letter guess from the player."""
    while True:
        guess = input("\nGuess a letter: ").strip().upper()
        if not guess.isalpha():
            print("Invalid input. Please enter a letter.")
        elif guess == "" or len(guess) > 1:
            print("Invalid input. Please enter only one letter.")
        elif guess in guessed_letters:
            print("You have already guessed this letter.")
        else:
            return guess


if __name__ == "__main__":
    """Start the game."""

    print("Welcome to Hangman!")
    while True:
        play_game()
        retry = input("\nWould you like to play again? (yes/no): ").lower()
        if retry not in {"yes", "y", 'ye'}:
            break
