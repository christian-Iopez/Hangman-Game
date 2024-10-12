from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)

words = [
    'python', 'flask', 'web', 'programming', 'hangman',
    'snake', 'coding', 'scripting', 'interpreter', 'module',
    'bottle', 'framework', 'server', 'routes', 'jinja',
    'html', 'browser', 'internet', 'client', 'css',
    'algorithm', 'software', 'function', 'variable', 'compiler',
    'guess', 'letter', 'puzzle', 'word', 'game',
    'debugging', 'loop', 'recursion', 'syntax', 'binary',
    'database', 'api', 'endpoint', 'cookies', 'session',
    'frontend', 'backend', 'middleware', 'javascript', 'query',
    'console', 'terminal', 'shell', 'object', 'class',
    'data', 'array', 'list', 'dictionary', 'tuple',
    'deploy', 'debug', 'git', 'repository', 'commit',
    'http', 'url', 'dns', 'firewall', 'encryption'
]


hidden_word = ''
guessed_letters = []
attempts = 0

@app.route('/')
def home():
    return redirect(url_for('hangman_game'))

@app.route('/hangman_game')
def hangman_game():
    global hidden_word, guessed_letters, attempts
    hidden_word = random.choice(words)
    guessed_letters = []
    attempts = 0
    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts)

# TODO TASK 1
#  Implement logic that correctly processes the hidden_word and guessed_letters and
#  returns a string with letters revealed or hidden based on user guesses.
def get_display_word():
    global hidden_word, guessed_letters
    display_word = [letter if letter in guessed_letters else '_' for letter in hidden_word] #This creates a list of letter or underscored depending on guessed letters.
    return ' '.join(display_word) # This will join the list with spaces in between using .join

# TODO TASK 2
#  Ensure that guesses are only added if they haven’t already been guessed.
#  Ensure that the function returns True for correct guesses and False for incorrect guesses.
def check_correct_guess(input_letter):
    global guessed_letters

    input_letter = input_letter.lower()  # Handles Case insensitivity by using .lower

    if input_letter in guessed_letters:
        return True  # Checks if the letter has already been guessed

    guessed_letters.append(input_letter)  # Add to guessed letters

    # Either returns True or False depending on if it is in the hidden word or not
    return input_letter in hidden_word


# TODO TASK 3
#  Implement the logic that tracks the number of attempts and determines if
#  the player has lost (attempts ≥ 6).
def check_lose():
    global attempts

    if attempts >= 6: # This will check the number of attempts, if it's greater than 6 you lose
        return True  # Player has lost
    return False # The player still has not lost

# TODO TASK 4
#  Ensure that the function correctly checks if all letters in hidden_word are
#  in the guessed_letters.
def check_win():
    global hidden_word, guessed_letters

    for char in hidden_word: # This for will check if every letter in the hidden_word is in guessed_letters
        if char not in guessed_letters:
            return False  # Returns False if any letter is not guessed, the player hasn't won yet

    return True  # Returns True if all letters have been guessed, the player wins

@app.route('/guess', methods=['POST'])
def guess():
    global hidden_word, attempts

    guessed_letter = request.form['letter']

    if not check_correct_guess(guessed_letter):
        attempts += 1

    if check_lose():
        return render_template('lose.html', word=hidden_word)

    if check_win():
        return render_template('win.html', word=hidden_word)

    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts)

if __name__ == '__main__':
    app.run(debug=True)
