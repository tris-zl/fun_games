import random


def play():
    elements = ["r", "p", "s"]
    computer = random.choice(elements)
    user = input("\nChoose between rock, paper and scissors (r/p/s): ")
    if user in elements:
        who_wins(user, computer)
    else:
        print("Please type in a valid expression. ")
        play()


def who_wins(user_choice, computer_choice):
    if user_choice == computer_choice:
        print("Tie. ")
    elif (user_choice == "r" and computer_choice == "s") or \
            (user_choice == "p" and computer_choice == "r") or \
            (user_choice == "s" and computer_choice == "p"):
        print("You won! ")
    else:
        print("Sorry, you lost. Try again! ")
    play_again()


def play_again():
    again = input("Do you want to play again? (y/n) ")
    if again == "y":
        play()
    elif again != "y" and again != "n":
        print("Invalid answer. ")
        play_again()


play()
