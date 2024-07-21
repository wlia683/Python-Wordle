import random
import sys
import time
from globals import use_alternate_color_scheme, scored_game, name, score
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QStackedLayout,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PyQt5.QtCore import Qt

# Style sheet
TITLE_STYLE = """
QLabel {
    font-size: 32px;
}
"""

COMMON_STYLE = """
QWidget {
    background-color: #404040;
    color: white;
    font-size: 16px;
}

QPushButton {
    background-color: #606060;
    color: white;
    border: none;
    padding: 8px 16px;
    font-size: 16px;
    border-radius: 15px;
}

QPushButton:hover {
    background-color: #808080;
}

QLabel {
    font-size: 16px;
}

QCheckBox {
    font-size: 16px;
    color: white;
}
"""

NORMAL_CORRECT_PLACE = """
QLabel {  
    background-color: #00A2E8;
    color: white;
    font-size: 24px;
    font-weight: bold;
}
"""

ALTERNATE_CORRECT_PLACE = """
QLabel {  
    background-color: #538D4E;
    color: white;
    font-size: 24px;
    font-weight: bold;
}
"""

NORMAL_CORRECT_LETTER = """
QLabel {
    background-color: #F0981C;
    color: white;
    font-size: 24px;
    font-weight: bold;
}
"""

ALTERNATE_CORRECT_LETTER = """
QLabel {  
    background-color: #B59F3B;
    color: white;
    font-size: 24px;
    font-weight: bold;
}
"""

INCORRECT = """
QLabel {
    background-color: #3A3A3C;
    color: white;
    font-size: 24px;
    font-weight: bold
}
"""


class TitleScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        title_label = QLabel("This is NOT Wordle.")
        title_label.setStyleSheet(TITLE_STYLE)
        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)
        instructions_options_button = QPushButton("Instructions/Options")
        instructions_options_button.clicked.connect(self.view_instructions_options)
        highscores_button = QPushButton("High Scores")
        highscores_button.clicked.connect(self.view_highscores)
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.exit_game)
        self.start_time = None
        layout.addWidget(title_label)
        layout.addWidget(start_button)
        layout.addWidget(instructions_options_button)
        layout.addWidget(highscores_button)
        layout.addWidget(quit_button)
        self.setStyleSheet(COMMON_STYLE)
        self.setLayout(layout)

    def start_game(self):
        self.start_time = time.time()
        stacked_layout.setCurrentIndex(1)

    def view_instructions_options(self):
        stacked_layout.setCurrentIndex(2)

    def view_highscores(self):
        highscores_screen.update_scores(highscores_screen.highscores_layout)
        stacked_layout.setCurrentIndex(3)

    def exit_game(self):
        exit()


class InstructionsOptionsScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.instructions = QLabel()
        self.update_instructions()
        options_layout = QVBoxLayout()
        options_label = QLabel("Options")
        self.colors_checkbox = QCheckBox("Alternative color scheme")
        self.colors_checkbox.stateChanged.connect(self.toggle_color_scheme)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.return_to_menu)
        options_layout.addWidget(options_label)
        options_layout.addWidget(self.colors_checkbox)
        layout.addWidget(self.instructions)
        layout.addLayout(options_layout)
        layout.addWidget(back_button)
        self.setStyleSheet(COMMON_STYLE)
        self.setLayout(layout)

    def return_to_menu(self):
        stacked_layout.setCurrentIndex(0)

    def toggle_color_scheme(self, state):
        global use_alternate_color_scheme
        use_alternate_color_scheme = state == Qt.Checked
        self.update_instructions()

    def update_instructions(self):
        global use_alternate_color_scheme
        if use_alternate_color_scheme:
            self.instructions.setText(
                "Guess the five letter word within six attempts. Letters in the correct place turn GREEN, letters in the word but in the wrong place turn YELLOW."
            )
        else:
            self.instructions.setText(
                "Guess the five letter word within six attempts. Letters in the correct place turn BLUE, letters in the word but in the wrong place turn ORANGE."
            )


class HighScoresScreen(QWidget):
    def __init__(self):
        super().__init__()

        global name
        self.name = name
        self.layout1 = QVBoxLayout()
        self.title = QLabel("Current High Score")
        self.highscores_layout = QVBoxLayout()
        self.highscores_layout.setSpacing(10)

        self.name_label = QLabel(f"Current name: {self.name}")
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter name here")
        self.confirm_name_button = QPushButton("Change name")
        self.back_button = QPushButton("Back")

        self.layout1.addWidget(self.title)
        self.layout1.addLayout(self.highscores_layout)
        self.layout1.addWidget(self.name_label)
        self.layout1.addWidget(self.name_entry)
        self.layout1.addWidget(self.confirm_name_button)
        self.layout1.addWidget(self.back_button)

        with open("highscores.txt", "r") as file:
            self.highscore_record = file.read()  

        self.update_scores(self.highscores_layout)     

         

        self.setLayout(self.layout1)

        self.back_button.clicked.connect(self.return_to_menu)
        self.confirm_name_button.clicked.connect(self.change_name)
        self.name_entry.returnPressed.connect(self.change_name)

    def update_scores(self, highscores_layout):
        for i in reversed(range(highscores_layout.count())):
            layout_item = highscores_layout.itemAt(i)
            if layout_item.widget():
                layout_item.widget().deleteLater()


        for i, item in enumerate(self.highscore_record):
            player, score = item.strip().split(',')
            label = QLabel(f"{player} {score}")
            highscores_layout.addWidget(label)
        
    def return_to_menu(self):
        stacked_layout.setCurrentIndex(0)

    def change_name(self):
        if not(self.name_entry.text()):
            return

        self.name = self.name_entry.text()
        self.name_entry.clear()
        self.name_label.setText(f"Current name: {self.name}")

class SaveScoreScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.save_score_layout = QVBoxLayout()
        self.title = QLabel("Congratulations! New High Score.")
        
        self.message = QLabel("If you wish to save your score, please enter a name: ")

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter name here")
        self.confirm_button = QPushButton("Confirm")
        self.back_button = QPushButton("Back")

        self.save_score_layout.addWidget(self.title)
        self.save_score_layout.addWidget(self.name_entry)
        self.save_score_layout.addWidget(self.confirm_button)
        self.save_score_layout.addWidget(self.back_button)

        self.setLayout(self.save_score_layout)

        self.back_button.clicked.connect(self.return_to_menu)

    def return_to_menu(self):
        stacked_layout.setCurrentIndex(0)

class WordGuessingGame(QWidget):
    def __init__(self):
        super().__init__()

        with open("wordlist.txt", "r") as file:
            self.all_possible_wordlist = file.read().splitlines()

        with open("wordlistans.txt", "r") as file:
            self.answer_wordlist = file.read().splitlines()

        self.word = self.get_random_word(self.answer_wordlist)
        self.max_guesses = 6
        self.guesses = 0
        self.guessed_words = []
        self.game_won = False
        self.is_first_time = True
        self.alphabet_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.setStyleSheet(COMMON_STYLE)

        self.init_ui()

    def init_ui(self):

        BUTTON_STYLE = """
        QPushButton {
            background-color: #606060;
            color: white;
            border: none;
            padding: 8px 16px; 
            font-size: 16px;
            }
        QPushButton:hover {
            background-color: #808080;
        }
        """

        self.setWindowTitle("A game not called Wordle.")
        self.setStyleSheet("background-color: black;")
        self.setFixedSize(700, 700)

        global score
        self.score = score

        self.is_new_highscore = False

        self.end_time = None

        self.guess_attempts_layout = QVBoxLayout()
        self.word_labels = []

        self.alphabet_layout = QVBoxLayout()
        self.row_labels = []
        for i in range(3):
            self.create_alphabet1_labels(i)

        self.result_label = QLabel()

        self.guess_entry = QLineEdit()
        self.guess_entry.setPlaceholderText("Enter your guess here.")
        self.submit_button = QPushButton("Submit Guess")
        self.guessed_words_layout = QVBoxLayout()
        self.play_again_button = QPushButton("Play again")
        self.play_again_button.setEnabled(False)
        self.return_button = QPushButton("Main Menu")

        self.result_label.setStyleSheet("background-color: #505050; color: white;")
        self.guess_entry.setStyleSheet("background-color: white; color: black;")
        self.submit_button.setStyleSheet(BUTTON_STYLE)
        self.play_again_button.setStyleSheet(BUTTON_STYLE)
        self.return_button.setStyleSheet(BUTTON_STYLE)

        layout = QVBoxLayout()
        layout.addLayout(self.guess_attempts_layout)
        layout.addWidget(self.guess_entry)
        layout.addWidget(self.submit_button)
        layout.addLayout(self.guessed_words_layout)
        layout.addWidget(self.play_again_button)
        layout.addWidget(self.result_label)
        layout.addLayout(self.alphabet_layout)
        layout.addWidget(self.return_button)

        self.setLayout(layout)

        self.submit_button.clicked.connect(self.check_guess)
        self.guess_entry.returnPressed.connect(self.check_guess)
        self.play_again_button.clicked.connect(self.restart)
        self.return_button.clicked.connect(self.return_to_menu)

    def get_random_word(self, words):
        return random.choice(words)

    def restart(self):
        self.word = self.get_random_word(self.answer_wordlist)
        self.guesses = 0
        self.guessed_words = []
        self.clear_words()
        self.play_again_button.setEnabled(False)
        self.submit_button.setEnabled(True)
        self.game_won = False
        self.is_first_time = True
        self.result_label.setText("")
        self.reset_alphabet()
        title_screen.start_time = time.time()
        self.is_new_highscore = False
  
    def clear_words(self):
        for i in reversed(range(self.guess_attempts_layout.count())):
            layout_item = self.guess_attempts_layout.itemAt(i)
            while layout_item.count():
                item = layout_item.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

    def create_word_labels(self):
        guess_layout = QHBoxLayout()  # Create a new QHBoxLayout for each guess attempt
        self.word_labels = []  # Clear previous word labels
        for letter in self.word:
            label = QLabel(letter)
            label.setFixedSize(40, 40)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px grey; background-color: black;")
            self.word_labels.append(label)
            guess_layout.addWidget(label)

        self.guess_attempts_layout.addLayout(
            guess_layout
        )  # Add the new QHBoxLayout to the main layout

    def create_alphabet1_labels(self, i):
        guess_layout = QHBoxLayout()
        row_labels = []  # Clear previous word labels
        for letter in self.alphabet_rows[i]:
            label = QLabel(letter)
            label.setFixedSize(40, 40)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                "background-color: #ADADAD; color: white; font-size: 24px; font-weight: bold"
            )
            row_labels.append(label)
            guess_layout.addWidget(label)

        self.alphabet_layout.addLayout(
            guess_layout
        )  # Add the new QHBoxLayout to the main layout
        self.row_labels.append(row_labels)

    def update_alphabet(self, guess):
        guess = guess.upper()
        word = self.word.upper()
        for i, row in enumerate(self.row_labels):
            for j, label in enumerate(row):
                letter = self.alphabet_rows[i][j]
                for k, guess_letter in enumerate(guess):
                    if guess_letter == word[k] == letter:
                        if use_alternate_color_scheme:
                            label.setStyleSheet(ALTERNATE_CORRECT_PLACE)
                        else:
                            label.setStyleSheet(NORMAL_CORRECT_PLACE)
                        print(
                            f"k = {k}, Processing guess_letter: {guess_letter}, alph_letter: {letter} guess: {guess}"
                        )
                    elif (guess_letter in word) & (guess_letter == letter):
                        if use_alternate_color_scheme:
                            label.setStyleSheet(ALTERNATE_CORRECT_LETTER)
                        else:
                            label.setStyleSheet(NORMAL_CORRECT_LETTER)
                    elif guess_letter == letter:
                        label.setStyleSheet(INCORRECT)

    def reset_alphabet(self):
        for row in self.row_labels:
            for label in row:
                label.setStyleSheet(
                    "background-color: grey; color: white; font-size: 24px; font-weight: bold"
                )

    def check_guess(self):
        guess = self.guess_entry.text().lower()
        if self.game_won:
            return

        if len(guess) != 5:
            self.display_result("Invalid word length.")
            self.guess_entry.clear()
            return

        if guess not in self.all_possible_wordlist:
            self.display_result("Not a valid word!")
            self.guess_entry.clear()
            return

        self.guesses += 1
        self.create_word_labels()  # Create new word labels for each guess attempt
        correct_place = self.display_word(guess, self.word)

        if correct_place == len(self.word):
            self.calculate_game_score()
            self.save_highscore()

            if self.is_new_highscore:
                self.display_result(f"Congratulations! New high score!\n\nYour score: {self.score}")
            else:
                self.display_result(f"Your score: {self.score}")

            self.guessed_words.append(self.word)
            self.submit_button.setEnabled(False)
            self.play_again_button.setEnabled(True)
            self.game_won = True

        elif self.guesses == self.max_guesses:
            self.display_result(f"You lose! The word was '{self.word}'.")
            self.submit_button.setEnabled(False)
            self.play_again_button.setEnabled(True)
            return
        else:
            self.display_result(f"Guesses left: {self.max_guesses - self.guesses}")

        self.update_alphabet(guess)
        self.guess_entry.clear()

    def display_word(self, guess, word):
        correct_place = 0
        correct_letter = 0
        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                self.word_labels[i].setText((letter.upper()))  # Show the guessed letter
                if use_alternate_color_scheme:
                    self.word_labels[i].setStyleSheet(ALTERNATE_CORRECT_PLACE)
                else:
                    self.word_labels[i].setStyleSheet(NORMAL_CORRECT_PLACE)
                correct_place += 1
            elif letter in self.word:
                self.word_labels[i].setText(letter.upper())  # Show the guessed letter
                if use_alternate_color_scheme:
                    self.word_labels[i].setStyleSheet(ALTERNATE_CORRECT_LETTER)
                else:
                    self.word_labels[i].setStyleSheet(NORMAL_CORRECT_LETTER)
                correct_letter += 1
            else:
                self.word_labels[i].setText(
                    letter.upper()
                )  # Clear any previous guessed letters
                self.word_labels[i].setStyleSheet(INCORRECT)
        return correct_place

    def display_result(self, text):
        self.result_label.setText(text)
        self.result_label.setStyleSheet(
            "background-color: #505050; font-size: 16px; color: white"
        )

    def return_to_menu(self):
        self.restart()
        stacked_layout.setCurrentIndex(0)

    def calculate_game_score(self):
        self.end_time = time.time()
        elapsed_time = self.end_time - title_screen.start_time
        time_penalty = elapsed_time * 1.5
        if self.guesses > 3:
            guess_penalty = self.guesses * 100
        else:
            guess_penalty = 0
        self.score = 2000 - time_penalty - guess_penalty
    
    def save_highscore(self):
        try:
            new_score = f"{highscores_screen.name},{round(self.score)}"
            if float(highscores_screen.highscore_record.split(",")[1]) < self.score:
                with open("highscores.txt", "w") as file:
                    file.write(new_score)
                highscores_screen.highscore_record = new_score
                self.is_new_highscore = True
        except (ValueError, IndexError):
        # If there is an error reading or comparing the high score, just save the new score
            with open("highscores.txt", "w") as file:
                file.write(new_score)
            highscores_screen.highscore_record = new_score
            self.is_new_highscore = True


if __name__ == "__main__":
    app = QApplication(sys.argv)

    game = WordGuessingGame()
    title_screen = TitleScreen()
    instructions_options_screen = InstructionsOptionsScreen()
    highscores_screen = HighScoresScreen()
    save_score_screen = SaveScoreScreen()

    stacked_layout = QStackedLayout()
    stacked_layout.addWidget(title_screen)
    stacked_layout.addWidget(game)
    stacked_layout.addWidget(instructions_options_screen)
    stacked_layout.addWidget(highscores_screen)
    stacked_layout.addWidget(save_score_screen)

    main_window = QWidget()
    main_window.setLayout(stacked_layout)
    main_window.setWindowTitle("This is NOT Wordle.")
    main_window.setGeometry(150, 150, 700, 700)
    main_window.setStyleSheet(COMMON_STYLE)
    main_window.show()

    sys.exit(app.exec_())
