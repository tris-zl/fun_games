from random_words import RandomWords


# create random word that is under 7 letters
def valid_word():
    rw = list((RandomWords().random_word()).casefold())
    while len(rw) > 6:
        rw = list((RandomWords().random_word()).casefold())
    return rw


def hangman():
    rw = valid_word()
    guesses = 10
    false_guesses = []

    # make list with length of rw
    my_word = []
    for _ in range(len(rw)):
        my_word.append("")

    print('\nIf you can guess the word already than ignore the "guess a letter"-request and type in "easy"')

    while guesses > 0 and my_word != rw:
        print(f'\n{guesses} guesses left. ')
        print(f'Your word: {my_word}')
        print(f'Already used letters that were not right: {false_guesses}\n')

        guess = input("Guess a letter: ")

        # quick answer
        if guess == "easy":
            easy = list((input("Type in the whole word: ")).casefold())
            if easy == rw:
                my_word = easy
            else:
                print("False, keep going! ")
            guesses = guesses - 1

        # guess for one letter
        else:
            if guess in rw:
                print("You guessed the right letter! ")
                # replace empty space(s) in my_word with the correctly guessed letter
                for i in range(len(rw)):
                    if rw[i] == guess:
                        my_word[i] = guess
            else:
                print("False, keep going. ")
                false_guesses.append(guess)
            guesses = guesses - 1

    if rw == my_word:
        print(f'\n\nGreat, you won! Needed guesses: {10 - guesses}')
    else:
        print("\n\nSorry, you have no more guesses left. Consider playing again! ")
        word = ''.join(rw)
        print(f'Correct word: {word}')


hangman()
