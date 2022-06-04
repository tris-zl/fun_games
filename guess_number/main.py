import random

try:
    guesses = 0
    right_num = random.randint(-100, 100)
    guess_num = int(input("Guess the number correctly: "))

    while not guess_num == right_num:
        guesses = guesses + 1
        if guess_num > right_num:
            print("The number is smaller than the one you typed in.")
            guess_num = int(input("Another try: "))
        elif guess_num < right_num:
            print("The number is bigger than the one you typed in.")
            guess_num = int(input("Another try: "))
    print(f'Congrats, you guessed the right number in {guesses} guesses!')

except ValueError as value_err:
    print(value_err)
